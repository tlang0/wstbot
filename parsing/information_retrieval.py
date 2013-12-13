########################################################################
# Copyright 2012 wst, wstcode@gmail.com
#
# This file is part of wstbot.
#
# wstbot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wstbot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with wstbot.  If not, see <http://www.gnu.org/licenses/>.
########################################################################

import os
import os.path
import yaml
import re
import logging
import sqlite3
import lxml.html
from parsing.parser import Parser
from util import (parse_for_url, unescape, get_modules_objects, 
                  first, chain_call, download_page, download_page_decoded)
from wstbot_locals import WEB_ENCODING, URL_REGEX_PREFIX

logger = logging.getLogger("wstbot")

# paths
MEDIA_DB_PATH = os.path.join("data", "media.db")
SITEINFO_FILE_PATH = os.path.join("data", "siteinfo.yaml")
SOURCES_PATH = os.path.join("parsing", "information_retrieval_sources")

# what kinds of links should be stored?
STORE_IMAGES = True
STORE_LINKS = True # meaning all other links
ITEMS_PER_PAGE = 15

# siteinfo stuff
FIRST_COLOR = "purple"
FIRST_STYLE = "bold"
REST_COLOR = "green"
REST_STYLE = "default"

class InformationRetrieval(Parser):

    def __init__(self, *args):
        super().__init__(*args)

        self.media = self.init_media()
        self.siteinfo = Siteinfo(self.msg_formats)

        self.sources = get_modules_objects(SOURCES_PATH, f=lambda x: x(self.bot))

    def init_media(self):
        if not os.path.exists(MEDIA_DB_PATH):
            logger.warning("Path does not exist: {0}. Did you forget to run the setup?"
                    .format(os.path.abspath(MEDIA_DB_PATH)))
            return None
        return Media(self.msg_formats)

    def parse(self, msg, nick):
        url = parse_for_url(msg)
        if url is None:
            return

        source = None
        info = None
        title = None

        def info_from_sources():
            nonlocal source
            for s in self.sources:
                info = s.find_info(url)
                if info is not None:
                    source = s
                    return info
            return None

        # try to find info by using the source modules
        info_from_modules = lambda: info_from_sources()
        # find infos using siteinfo object
        info_from_siteinfo = lambda: self.siteinfo.find_info(url)
        # try them in order; if the first one succeeds, the second one is not called
        r = info_from_modules() or info_from_siteinfo() 
        if r is not None:
            info, title = r
            logger.debug("title: {}".format(title))

        if msg.strip()[-1] != "#":
            # store media
            if source is not None:
                # use the media handler of the object that was used for information retrieval
                type_, url = source.find_media_info(url)
                self.media.store_media(url, title=title, type_=type_)
            else:
                # use the builtin media handlers
                self.media.store_media(url, title=title)

        return info

class Siteinfo:

    def __init__(self, msg_formats):
        self.sitedata = None
        self.msg_formats = msg_formats
        self.mtime = None
        self.load_yaml_siteinfo()

    def load_yaml_siteinfo(self):
        mtime = os.path.getmtime(SITEINFO_FILE_PATH)
        if self.mtime is None or mtime > self.mtime:
            # load siteinfo data
            with open(SITEINFO_FILE_PATH, "r") as siteinfo_file:
                self.sitedata = yaml.safe_load(siteinfo_file)
            self.mtime = os.path.getmtime(SITEINFO_FILE_PATH)

    def patterns_for_url(self, url):
        """Get the information dict from the yaml file for the url contained in msg.
        Returns a tuple (url, resource_dict) where info is the yaml dict"""

        # reload siteinfo data if it has changed
        self.load_yaml_siteinfo()
                
        for resource_dict in self.sitedata["sources"]:
            try:
                match = re.search(resource_dict["url pattern"], url)
            except:
                logger.warning("Bad url pattern: " + resource_dict["url pattern"])
                continue
            if not match:
                continue

            url = match.group(1)
            logger.info("Found siteinfo url for " + resource_dict["name"] + "!")
            logger.info("url: " + url)

            return (url, resource_dict)

    def search_site(self, url, resource_dict):
        """Downloads the URL's content, searches for the paths and patterns
        and builds a message out of the matched data.

        Arguments: resource_dict contains the paths, patterns and additional data for
        the url.
        """

        if self.sitedata is None:
            return

        # retrieve content
        content = download_page(url).decode(WEB_ENCODING, "replace")
        if content is None:
            return

        message = None
        title = None

        def info_xpath():
            # try to find info using xpath
            root = lxml.html.fromstring(content)
            items = root.xpath(info["xpath"])
            logger.debug("using xpath: " + info["xpath"])
            if items is not None and len(items) >= 1:
                return items[0]
            else:
                return None

        def info_regex():
            # try to find info using a regex pattern
            logger.debug("using regex: " + info["pattern"])
            match = re.search(info["pattern"], content)
            if match is None:
                logger.warning("Could not find info! (match == None) with pattern: " + info["pattern"])
                return None
            if match.groups() is None:
                logger.warning("match.groups() was None")
                return None
            if len(match.groups()) <= 0:
                logger.warning("Found match but no groups")
                return None

            return match.group(1)

        for info in resource_dict["patterns"]:
            if not "pattern" in info and not "xpath" in info:
                logger.error("siteinfo entry does not contain a path or pattern!")
                break

            infodata = None
            # try regex first because it seems to be faster
            if "pattern" in info:
                infodata = info_regex()
            # try xpath if there was no pattern or regex was unsuccessful
            if infodata is None and "xpath" in info:
                infodata = info_xpath()

            if infodata is None:
                logger.warning("infodata was None!")
                break

            logger.debug("\ninfodata:\n")
            logger.debug(infodata)

            if infodata is None or infodata == "":
                continue

            logger.info("found info data: " + infodata)
            infodata = unescape(infodata)

            infodata = infodata.strip()
            if title is None:
                title = infodata
                
            color = REST_COLOR
            style = REST_STYLE
            if message is None:
                message = ""
                color = FIRST_COLOR
                style = FIRST_STYLE
            message += self.msg_formats.get(style, self.msg_formats.get(color, infodata))
            if info != resource_dict["patterns"][-1]:
                message += " " + self.sitedata["separator"] + " "

        # cut last separator if there is one
        sep = self.sitedata["separator"]
        if message is not None and message.strip()[-len(sep):] == sep:
            message = message.strip()[:-len(sep)].strip()
            
        return message, title

    def find_info(self, url):
        """Find information in the page at the specified url."""
        r = self.patterns_for_url(url)
        if r is None:
            return
        url, resource_dict = r
        return self.search_site(url, resource_dict)

class Media:
    """Parse for URLs that could be of interest and store them"""

    def __init__(self, msg_formats):
        self.msg_formats = msg_formats
        
    def store_media(self, url, title=None, type_=None):
        if type_ is None:
            # try the builtin types
            media_info = chain_call(url, [self.parse_image, self.parse_link])
            if media_info is None:
                logger.warning("media was not stored")
                return 
            type_, url = media_info

        if title is None:
            title = ""

        # write
        with sqlite3.connect(MEDIA_DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("insert into media (type, title, url) values (?, ?, ?)",
                    (type_, title, url))
            conn.commit()

    def parse_link(self, url):
        if not STORE_LINKS:
            return None

        return ("link", url)

    def parse_image(self, url):
        if not STORE_IMAGES:
            return None

        # prefix for URLs in general
        match = re.search("(" + URL_REGEX_PREFIX + ".*(\.jpeg|\.jpg|\.png|\.gif))", url)
        if match is None:
            return None

        logger.info("Found image url: " + url)
        return ("image", url)

CLASS_ = InformationRetrieval

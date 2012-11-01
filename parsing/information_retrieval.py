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
import yaml
import re
import logging
import sqlite3
from parsing.parser import Parser
from util import (parse_for_url, unescape, get_directory_modules_objects, 
                  first, chain_call, download_page, download_page_decoded)
from wstbot_locals import WEB_ENCODING, URL_REGEX_PREFIX

# paths
MEDIA_DB_PATH = os.path.join("data", "media.db")
REGEX_FILE_PATH = os.path.join("data", "regex.yaml")
SOURCES_PATH = os.path.join("parsing", "information_retrieval_sources")

# what kinds of links should be stored?
STORE_IMAGES = True
STORE_YOUTUBE = True
STORE_LINKS = True # meaning all other links
ITEMS_PER_PAGE = 15

class InformationRetrieval(Parser):

    def __init__(self, *args):
        super().__init__(*args)

        self.media = self.init_media()
        self.regex = Regex(self.msg_formats)

    def init_media(self):
        if not os.path.exists(MEDIA_DB_PATH):
            logging.warning("Path does not exist: {0}. Did you forget to run the setup?"
                    .format(os.path.abspath(MEDIA_DB_PATH)))
            return None
        return Media(self.msg_formats)

    def parse(self, msg, nick):
        url = parse_for_url(msg)
        if url is None:
            return

        sources = get_directory_modules_objects(SOURCES_PATH)

        # try to find info by using the source modules
        info_from_modules = lambda: first((source.retrieve_information(url) for source in sources))
        # find infos using regex patterns
        info_from_regex = lambda: self.regex.find_info(url)
        # try them in order; if the first one succeeds, the second one is not called
        info = info_from_modules() or info_from_regex() 

        # store media
        self.media.store_media(url, title=info)

        return info

class Regex:

    def __init__(self, msg_formats):
        self.regexdata = None
        self.msg_formats = msg_formats

    def patterns_for_url(self, url):
        """Get the information dict from the yaml file for the url contained in msg.
        Returns a tuple (url, resource_dict) where info is the yaml dict"""

        # load regex strings
        with open(REGEX_FILE_PATH, "r") as regex_file:
            self.regexdata = yaml.safe_load(regex_file)
        
        for resource_dict in self.regexdata["sources"]:
            try:
                match = re.search(resource_dict["url pattern"], url)
            except:
                logging.warning("bad regex: " + resource_dict["url pattern"])
                continue
            if not match:
                continue

            url = match.group(1)
            logging.info("Found information from " + resource_dict["name"] + "!")
            logging.info("url: " + url)

            return (url, resource_dict)

    def do_regex(self, url, resource_dict, name_and_title=False):
        """Downloads the URL's content, searches for the regular expressions
        and builds a message out of the matched data.

        Arguments: resource_dict contains the patterns and additional data for
        the url.

        If name_and_title is set, only the name and the result of the first
        pattern match (wich is usually the title of the article) will be 
        returned: (name, title)
        """

        if self.regexdata is None:
            return

        # retrieve content
        content = download_page(url).decode(WEB_ENCODING, "replace")
        if content is None:
            return

        message = None

        for info in resource_dict["patterns"]:
            # try to find info
            match = re.search(info["pattern"], content)
            if match is None:
                logging.warning("Could not find info! (match == None)")
                break
            if match.groups() is None:
                logging.warning("match.groups() was None")
                break
            if len(match.groups()) <= 0:
                logging.warning("Found match but no groups")
                break

            infodata = match.groups()[0]
            logging.info("found info data: " + infodata)
            infodata = unescape(infodata)

            # name and title
            if name_and_title:
                return (resource_dict["name"], infodata)

            if "replace" in info:
                infodata = self.do_replace(infodata, info["replace"])

            infodata = infodata.strip()
                
            if message is None:
                message = ""
            message += self.msg_formats.get(info["style"], self.msg_formats.get(info["color"], infodata))
            if info != resource_dict["patterns"][-1]:
                message += " " + self.regexdata["separator"] + " "

        # cut last separator if there is one
        sep = self.regexdata["separator"]
        if message is not None and message.strip()[-len(sep):] == sep:
            message = message.strip()[:-len(sep)].strip()
            
        return message

    def find_info(self, url, name_and_title=False):
        """Find information in the page at the specified url."""
        r = self.patterns_for_url(url)
        if r is None:
            return
        url, resource_dict = r
        output = self.do_regex(url, resource_dict, name_and_title=name_and_title)
        return output
            
    def do_replace(self, message, replacements):
        newmessage = message
        for replacedata in replacements:
            if not "needle" in replacedata or not "replacement" in replacedata:
                logging.warning("replace: no needle or no replacement specified")
            else:
                newmessage = newmessage.replace(replacedata["needle"], replacedata["replacement"])

        return newmessage


class Media:
    """Parse for URLs that could be of interest and store them"""

    def __init__(self, msg_formats):
        self.msg_formats = msg_formats
        
    def store_media(self, url, title=None):
        media_info = chain_call(url, [self.parse_image, self.parse_youtube, self.parse_link])
        # something went wrong
        if media_info is None:
            logging.debug("media_info was None")
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

        def imgur(url):
            logging.info("found imgur url")
            content = download_page_decoded(url)
            match1 = re.search('<a href="(.*)" target="_blank">View full resolution', content)
            match2 = re.search('<link rel="image_src" href="(.*)"\s*/>', content)
            match = match1 or match2
            if match:
                logging.info("imgur match")
                imageurl = match.group(1)
                if imageurl:
                    return imageurl
            else:
                return None

        # prefix for URLs in general
        match = re.search("(" + URL_REGEX_PREFIX + ".*(\.jpeg|\.jpg|\.png|\.gif))", url)
        imgurmatch = re.search("(" + URL_REGEX_PREFIX + "imgur.com/(.*/)?((\d|\w)*)(/)?)", url)
        if imgurmatch:
            url = imgur(imgurmatch.group(1))

        if match is None and imgurmatch is None:
            return None

        logging.info("Found image url: " + url)
        return ("image", url)

    def parse_youtube(self, url):
        if not STORE_YOUTUBE:
            return None

        match_youtube = re.search(URL_REGEX_PREFIX + "youtube\.com/watch.*v=(\S{11})", url)
        match_youtube_short = re.search(URL_REGEX_PREFIX + "youtu\.be/(\S+)", url)
        match = match_youtube or match_youtube_short
        if match is None:
            return
        video_id = match.group(1)

        logging.info("Found youtube video: " + video_id)
        return ("youtube", video_id)

CLASS_ = InformationRetrieval

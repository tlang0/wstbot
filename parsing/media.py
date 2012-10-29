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

# -*- coding: utf-8 -*-

import os
import re
import json
import urllib.request
import html
import sqlite3
from util import str_list_to_int, parse_for_url, download_page_decoded
from parsing.parser import Parser
from wstbot_locals import URL_REGEX_PREFIX

# what kinds of links should be stored?
STORE_IMAGES = True
STORE_YOUTUBE = True
STORE_LINKS = True # meaning all other links
ITEMS_PER_PAGE = 15

MEDIA_DB_PATH = os.path.join("data", "media.db")

class Media(Parser):
    """Parse for URLs that could be of interest and store them"""
    
    def __init__(self, *args):
        super().__init__(*args)

        if not os.path.exists(MEDIA_DB_PATH):
            self.logger.warning("Path does not exist: " + os.path.abspath(MEDIA_DB_PATH))
            self.enabled = False
            return

        self.items = 0
        
    def parse(self, msg, nick):
        print("PARSING A LINK\n#########################")
        url = parse_for_url(msg)
        # no link found
        if url is None:
            return

        media_info = self.chain_parse(url, [self.parse_image, self.parse_youtube, self.parse_link])
        # something went wrong
        if media_info is None:
            self.logger.debug("media_info was None")
            return 
        type_, url = media_info

        # try to find a title
        title = self.try_get_title(type_, url)
        if title is None:
            title = ""

        # write
        with sqlite3.connect(MEDIA_DB_PATH) as conn:
            cur = conn.cursor()
            d = media_info_dict
            cur.execute("insert into media (type, title, url) values (?, ?, ?)",
                    (type_, title, url))
            conn.commit()

        self.items += 1

    def try_add_title(self, type_, url):
        """Try to find a description for the link using the regex module
        and add it to media_info_dict"""
        try:
            import parsing.regex
        except ImportError:
            return

        regex_parser = parsing.regex.Regex(self.bot, self.logger)
        if type_ == "youtube":
            url = "http://www.youtube.com/watch?v=" + url
        # get the resource name and title
        data = regex_parser.find_info(url, name_and_title=True)
        if data is not None:
            return html.escape(data[1]) # title

    def parse_link(self, url):
        if not STORE_LINKS:
            return None

        return ("link", url)

    def parse_image(self, url):
        if not STORE_IMAGES:
            return None

        def imgur(url):
            self.logger.info("found imgur url")
            content = download_page_decoded(url)
            match1 = re.search('<a href="(.*)" target="_blank">View full resolution', content)
            match2 = re.search('<link rel="image_src" href="(.*)"\s*/>', content)
            match = match1 or match2
            if match:
                self.logger.info("imgur match")
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

        self.logger.info("Found image url: " + url)
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

        self.logger.info("Found youtube video: " + video_id)
        return ("youtube", video_id)

    def chain_parse(self, url, functions):
        r = None
        for f in functions:
            r = f(url)
            if r is not None:
                break
        return r

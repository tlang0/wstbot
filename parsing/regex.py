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

import urllib.request
import re
import yaml
import html.parser
import os
import util
from parsing.parser import Parser

WEB_ENCODING = "utf-8"
REGEX_FILE = os.path.join("data", "regex.yaml")

class Regex(Parser):

    def __init__(self, *args):
        super().__init__(*args)
        self.regexdata = None

    def patterns_for_url(self, msg):
        """Get the information dict from the yaml file for the url contained in msg.
        Returns a tuple (url, resource_dict) where info is the yaml dict"""

        # valid ?
        msg_url = util.parse_for_url(msg)
        if msg_url is None:
            return

        self.logger.info("last message was a link!")

        # load regex strings
        with open(REGEX_FILE, "r") as regex_file:
            self.regexdata = yaml.safe_load(regex_file)
        
        for resource_dict in self.regexdata["sources"]:
            try:
                match = re.search(resource_dict["url pattern"], msg_url)
            except:
                self.logger.warning("bad regex: " + resource_dict["url pattern"])
                continue
            if not match:
                continue

            url = match.group(1)
            self.logger.info("Found information from " + resource_dict["name"] + "!")
            self.logger.info("url: " + url)

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

        try:
            site = urllib.request.urlopen(url)
        except:
            self.logger.warning("Error opening url!")
            return

        # retrieve content
        content = site.read().decode(WEB_ENCODING, "replace")

        message = None

        for info in resource_dict["patterns"]:
            # try to find info
            match = re.search(info["pattern"], content)
            if match is None:
                self.logger.warning("Could not find info! (match == None)")
                break
            if match.groups() is None:
                self.logger.warning("match.groups() was None")
                break
            if len(match.groups()) <= 0:
                self.logger.warning("Found match but no groups")
                break

            infodata = match.groups()[0]
            self.logger.info("found info data: " + infodata)
            infodata = self.unescape(infodata)

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

    def find_info(self, string, name_and_title=False):
        """Find the wanted information using the regular expressions"""
        r = self.patterns_for_url(string)
        if r is None:
            return
        url, resource_dict = r
        output = self.do_regex(url, resource_dict, name_and_title=name_and_title)
        return output
            
    def parse(self, msg, nick):
        return self.find_info(msg)

    def do_replace(self, message, replacements):
        newmessage = message
        for replacedata in replacements:
            if not "needle" in replacedata or not "replacement" in replacedata:
                self.logger.warning("replace: no needle or no replacement specified")
            else:
                newmessage = newmessage.replace(replacedata["needle"], replacedata["replacement"])

        return newmessage

    def unescape(self, message):
        parser = html.parser.HTMLParser()
        return parser.unescape(message)

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
from colors import colors, styles

#URL_PREFIX = '(https?://)(www\.)?'
WEB_ENCODING = "utf-8"
REGEX_FILE = os.path.join("data", "regex.yaml")

class Regex:

    def __init__(self):
        self.regexdata = None

    def patterns_for_url(self, msg):
        """Get the information dict from the yaml file for the url contained in msg.
        Returns a tuple (url, resource_dict) where info is the yaml dict"""

        # do not display
        if msg[-1] == '*':
            return

        # valid ?
        if not "http://" in msg and not "www" in msg:
            return

        # load
        fp = open(REGEX_FILE, "r")
        self.regexdata = yaml.safe_load(fp)
        fp.close()
        
        try:
            url_match = re.search("((https?://)(www\.)?\S+)", msg)
            msg_url = url_match.group(1)
        except:
            print("no link found")
            return

        for resource_dict in self.regexdata["sources"]:
            try:
                match = re.search(resource_dict["url pattern"], msg_url)
            except:
                print("bad regex: " + resource_dict["url pattern"])
                continue
            if not match:
                continue

            url = match.groups()[0]
            print("Found news from " + resource_dict["name"] + "!")
            print("url: " + url)

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
            print("Error opening url!")
            return

        # retrieve content
        content = site.read().decode(WEB_ENCODING, "replace")

        message = None

        for info in resource_dict["patterns"]:
            # try to find info
            match = re.search(info["pattern"], content)
            if match is None:
                print("Could not find info! (match == None)")
                break
            if match.groups() is None or match.groups()[0] is None:
                print("Found match but no groups")
                try:
                    print("the pattern was: " + info["pattern"])
                    print("match.groups(): " + str(match.groups()))
                    print("match.group(0): " + str(match.group(0)))
                    print("match.group(1): " + str(match.group(1)))
                except IndexError:
                    pass
                break

            infodata = match.groups()[0]
            print("found info data: " + infodata)
            infodata = self.unescape(infodata)

            # name and title
            if name_and_title:
                return (resource_dict["name"], infodata)

            if "replace" in info:
                infodata = self.do_replace(infodata, info["replace"])

            infodata = infodata.strip()
                
            if message is None:
                message = ""
            message += styles[info["style"]] + colors[info["color"]] + infodata 
            if info != resource_dict["patterns"][-1]:
                message += " " + styles["default"] + colors["default"] + self.regexdata["separator"] + " "

        # cut last separator if there is one
        sep = self.regexdata["separator"]
        if message is not None and message.strip()[-len(sep):] == sep:
            message = message.strip()[:-len(sep)].strip()
            
        return message
            
    def parse(self, bot, msg, nick):
        r = self.patterns_for_url(msg)
        if r is None:
            return
        url, resource_dict = r
        message = self.do_regex(url, resource_dict)
        return message

    def do_replace(self, message, replacements):
        newmessage = message
        for replacedata in replacements:
            if not "needle" in replacedata or not "replacement" in replacedata:
                print("replace: no needle or no replacement specified")
            else:
                newmessage = newmessage.replace(replacedata["needle"], replacedata["replacement"])

        return newmessage

    def unescape(self, message):
        parser = html.parser.HTMLParser()
        return parser.unescape(message)

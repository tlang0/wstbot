# -*- coding: utf-8 -*-

import urllib.request
import re
import yaml
import html.parser
from colors import colors, styles

#URL_PREFIX = '(https?://)(www\.)?'
WEB_ENCODING = "utf-8"
REGEX_FILE = "regex.yaml"

class Regex:

    def parse(self, bot, msg, nick):
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

        for source in self.regexdata["sources"]:
            try:
                match = re.search(source["url pattern"], msg_url)
            except:
                print("bad regex: " + source["url pattern"])
                continue
            if not match:
                continue
            url = match.groups()[0]
            print("Found news from " + source["name"] + "!")
            print("url: " + url)
        
            try:
                site = urllib.request.urlopen(url)
            except:
                print("Error opening url!")
                return

            # retrieve content
            content = site.read().decode(WEB_ENCODING, "replace")

            message = None

            for info in source["patterns"]:
                # try to find info
                match = re.search(info["pattern"], content)
                if match is None:
                    print("Could not find info! (match == None)")
                    return message
                if match.groups() is None or match.groups()[0] is None:
                    print("Found match but no groups")
                    try:
                        print("the pattern was: " + info["pattern"])
                        print("match.groups(): " + str(match.groups()))
                        print("match.group(0): " + str(match.group(0)))
                        print("match.group(1): " + str(match.group(1)))
                    except IndexError:
                        pass
                    return message

                infodata = match.groups()[0]
                print("found info data: " + infodata)
                infodata = self.unescape(infodata)

                if "replace" in info:
                    infodata = self.do_replace(infodata, info["replace"])

                infodata = infodata.strip()
                    
                if message is None:
                    message = ""
                message += styles[info["style"]] + colors[info["color"]] + infodata 
                if info != source["patterns"][-1]:
                    message += " " + styles["default"] + colors["default"] + self.regexdata["separator"] + " "
                
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

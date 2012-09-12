# -*- coding: utf-8 -*-

import urllib2
import re
import HTMLParser
import json
from colors import C

MESSAGE = C.BOLD + C.RED + "#TITLE" + C.NOFO
MESSAGE_AUTHOR = MESSAGE + " :: " + C.GREEN + "#AUTHOR" + C.NOFO
URL_PREFIX = '(https?://)(www\.)?'

class News:

    def __init__(self):
        self.news = json

    def parse(self, bot, msg, nick):
        # do not display
        if msg[-1] == '*':
            return

        # valid ?
        if not "http://" in msg and not "www" in msg:
            return

        # load
        fp = open("REGEX", "r")
        self.news = json.load(fp)
        fp.close()
        
        try:
            url_match = re.search("((https?://)(www\.)?\S+)", msg)
            msg_url = url_match.group(1)
        except:
            print("no link found")
            return

        for news in self.news:
            try:
                match = re.search(news[1], msg_url)
            except:
                print("shitty regex: " + news[1])
                continue
            if not match:
                continue
            url = match.groups()[0]
            print("Found news from " + news[0] + "!")
            print("url: " + url)
        
            try:
                site = urllib2.urlopen(url)
            except:
                print("Error opening url!")
                return

            # retrieve content
            content = site.read()

            # try to find title
            match = re.search(news[2], content)
            if match is None:
                print("Could not find title! (match == None)")
                return
            if match.groups() is None or match.groups()[0] is None:
                print("Found match but no groups")
                try:
                    print("the pattern was: " + news[2])
                    print("match.groups(): " + str(match.groups()))
                    print("match.group(0): " + str(match.group(0)))
                    print("match.group(1): " + str(match.group(1)))
                except IndexError:
                    pass
                return

            title = match.groups()[0]
            title = self.specialchars(title)
            print("found title: " + title)

            message = MESSAGE

            # try to find author
            if len(news) > 3:
                match = re.search(news[3], content)
                if not match:
                    print("Author regex was specified but could not be found")
                else:
                    message = MESSAGE_AUTHOR
                    message = message.replace("#AUTHOR", match.groups()[0])

            message = message.replace("#TITLE", title)

            return message


    def specialchars(self, text):
        #text = text.replace('&uuml;', 'ü')
        #text = text.replace('&auml;', 'ä')
        #text = text.replace('&ouml;', 'ö')
        #text = text.replace('&#xFC;', 'ü')
        #text = text.replace('&#xF6;', 'ö')
        #text = text.replace('&#xE4;', 'ä')
        parser = HTMLParser.HTMLParser()
        decoded = text
        try:
            decoded = parser.unescape(text)
        except:
            print("could not unescape text")
        return decoded


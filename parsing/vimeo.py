# -*- coding: utf-8 -*-

import re, urllib2, json
from colors import C

ERROR_MESSAGE = "An error occured while retrieving information about the vimeo video."
VIDEO_MESSAGE = C.BOLD + C.VIOLET \
        + "#TITLE" + C.NOFO + C.BLACK + " :: " + C.GREEN + "#DURATION"

class Vimeo(object):

    def parse(self, bot, msg, nick):
        if msg[-1] == "*" or not "vimeo." in msg:
            return

        # video id
        match = re.search('vimeo\.com/(.*)', msg)
        if not match or not match.groups()[0]:
            return

        video_id = match.groups()[0]
        print("found vimeo video id: " + video_id)
             
        url_video_data = "http://vimeo.com/api/v2/video/" + video_id + ".json"
        try:
            content_json = urllib2.urlopen(url_video_data)
            content_json = content_json.read()
        except:
            print("an error occurred during urlopen!")

        content = json.loads(content_json)
        content = content[0]
    
        title = content["title"]
        secs = int(content["duration"])
        duration = str(secs / 60) + "m " + str(secs % 60) + "s"

        message = VIDEO_MESSAGE.replace("#TITLE", title)
        message = message.replace("#DURATION", duration)

        return message

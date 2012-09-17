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

import re
import urllib.request
import json
from colors import C

ERROR_MESSAGE = "An error occured while retrieving information about the vimeo video."
VIDEO_MESSAGE = C.BOLD + C.PURPLE \
        + "#TITLE" + C.NOFO + C.BLACK + " :: " + C.GREEN + "#DURATION"

class Vimeo:

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
            content_json = urllib.request.urlopen(url_video_data)
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

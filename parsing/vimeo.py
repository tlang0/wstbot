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
from parsing.parser import Parser

ERROR_MESSAGE = "An error occured while retrieving information about the vimeo video."
VIDEO_MESSAGE = C.BOLD + C.PURPLE + "{title}" + C.NOFO + C.BLACK + " :: " + C.GREEN + "{duration}"

class Vimeo(Parser):

    def parse(self, msg, nick):
        # get video id
        match = re.search('vimeo\.com/(\S*)', msg)
        if not match or not match.groups()[0]:
            return

        video_id = match.groups()[0]
        self.logger.info("found vimeo video id: " + video_id)
             
        url_video_data = "http://vimeo.com/api/v2/video/" + video_id + ".json"
        try:
            content = urllib.request.urlopen(url_video_data).read()
        except:
            self.logger.warning("an error occurred during urlopen!")
            return

        content = str(content, "utf-8")
        content_json = json.loads(content)
        content_json = content_json[0]
    
        title = content_json["title"]
        secs = int(content_json["duration"])
        duration = str(secs / 60) + "m " + str(secs % 60) + "s"

        message = VIDEO_MESSAGE.format(title=title, duration=duration)

        return message

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

import logging
import json
import re
from wstbot_locals import URL_REGEX_PREFIX
from util import download_page
from parsing.information_retrieval_sources.information_source import InformationSource

logger = logging.getLogger("wstbot")

class Vimeo(InformationSource):

    def __init__(self, *args):
        super().__init__(*args)
        self.video_id = None

    def find_info(self, url):
        # get video id
        match = re.match(URL_REGEX_PREFIX + 'vimeo\.com/(\S*)', url)
        if match is None:
            return

        self.video_id = match.group(1)
        logger.info("Found vimeo video: " + self.video_id)

        json_url = "http://vimeo.com/api/v2/video/{0}.json".format(self.video_id)
        json_content = download_page(json_url).decode("utf-8")
        json_data = json.loads(json_content)
        json_data = json_data[0]
    
        raw_title = json_data["title"]
        title = self.msg_formats.bold(self.msg_formats.red(raw_title))
        secs = int(json_data["duration"])
        duration = self.msg_formats.green(str(int(secs / 60)) + "m " + str(secs % 60) + "s")

        message = "{0} :: {1}".format(title, duration)

        return (message, raw_title)

    def find_media_info(self, url):
        if self.video_id is not None:
            return ("vimeo", self.video_id)
        else:
            return None

CLASS_ = Vimeo

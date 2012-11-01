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

import re
from wstbot_locals import URL_REGEX_PREFIX
from parsing.parser import Parser

OH_NO = "Your XMPP client doesn't show images."

class ImageDisplay(Parser):
    
    def parse(self, msg, nick):
        img_url_match = re.search(URL_REGEX_PREFIX + "\S+\.(png|jpg|jpeg|gif)", msg)
        if img_url_match:
            img_url = img_url_match.group(0)
            return '<img src="{0}" alt="{1}" />'.format(img_url, OH_NO)

CLASS_ = ImageDisplay

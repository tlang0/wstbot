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
import urllib.request
from wstbot_locals import URL_REGEX_PREFIX
from wstbot_locals import WEB_READ_MAX, WEB_ENCODING

def download_page_decoded(url):
    return download_page(url).decode(WEB_ENCODING)

def download_page(url):
    return urllib.request.urlopen(url).read(WEB_READ_MAX)

def parse_for_url(message):
    """Try to find a URL in the message."""

    match = re.search(URL_REGEX_PREFIX + "\S+", message)
    if match is not None:
        return match.group(0)
    return None

def apply_seq(function, sequence):
    """Applies a function to every element of the sequence"""
    for item in sequence: 
        function(item)

def str_list_to_int(l):
    """Converts a list of strings to a list of integers"""
    new_list = []
    for e in l:
        try:
            e = int(e)
        except:
            continue
        else:
            new_list.append(e)

    return new_list

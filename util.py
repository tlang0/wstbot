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
import os
import re
import urllib.request
import importlib
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

def objects_from_files(directory, f=None):
    """
    1. Read files from a folder
    2. Create objects from the classes contained in the files which should
       have the same name as the file, with the first letter in upper case

       - f is the function that is used to instantiate the class and is
       called with the class as argument: f(class)
    """

    if f is None:
        f = lambda c: c()
    
    objects = []

    # Load object objects
    for objectfile in os.listdir(directory):
        if objectfile[-2:] != "py" or objectfile[0] in [".", "_"]:
            continue

        objectclass = objectfile[0].upper() + objectfile[1:objectfile.rfind('.')]
        objectmodule = objectclass.lower()

        # omit templates (abstract classes)
        if objectmodule == "command" or objectmodule == "parser":
            continue

        try:
            logging.info("Importing object '" + objectclass + "'...")
            module = importlib.import_module("{0}.{1}".format(directory, objectmodule))
            class_ = getattr(module, objectclass)
            obj = f(class_)
            objects.append(obj)
        except ImportError as err:
            logging.warning("Importing '{0}' from '{1}' was unsuccessful!".format(objectclass, objectfile))
            logging.warning("Reason: {}".format(err))

    return objects

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
import glob
import html.parser
from wstbot_locals import WEB_READ_MAX, WEB_ENCODING, URL_REGEX_PREFIX

logger = logging.getLogger("wstbot")

def unescape(message):
    parser = html.parser.HTMLParser()
    return parser.unescape(message)

def download_page_decoded(url):
    return download_page(url).decode(WEB_ENCODING)

def download_page(url):
    try:
        return urllib.request.urlopen(url).read(WEB_READ_MAX)
    except:
        logger.warning("Error opening url / downloading content!")
        return None

def parse_for_url(message):
    """Try to find a URL in the message."""

    match = re.search(URL_REGEX_PREFIX + "\S+", message)
    if match is not None:
        return match.group(0)
    return None

def first(sequence):
    """Returns the first encountered element in the sequence that is not None."""
    if sequence is None:
        return None
    for e in sequence:
        if e is not None:
            return e
    return None

def chain_call(value, functions):
    """Calls every function in functions with the value and returns the first result
    that is not None. Returns None if all functions returned None."""
    for f in functions:
        r = f(value)
        if r is not None:
            return r
    return None

def apply_seq(function, sequence):
    """Applies a function to every element of the sequence"""
    for e in sequence: 
        function(e)

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

def get_modules(path):
    """Return a list of python modules in a given path. 
    Files not ending with '.py' are ignored. 
    May throw an OSError."""

    modules = []

    module_path = path.replace(os.sep, ".")
    importlib.import_module(module_path)

    # get file names
    filenames = glob.glob(os.path.join(path, "*.py"))
    filenames = (os.path.basename(x) for x in filenames)
    # get module names
    module_names = (os.path.splitext(x)[0] for x in filenames)
    # import modules
    for module_name in module_names:
        # ignore __init__ and so on:
        if module_name[1] == "_":
            continue

        try:
            logger.info("Importing module '" + module_name + "'...")
            modules.append(importlib.import_module("." + module_name, module_path))
        except ImportError as err:
            logger.warning("Importing '{0}' was unsuccessful!".format(module_path + "." + module_name))
            logger.warning("Reason: {0}".format(err))

    return modules

def get_modules_objects(path, f=lambda x: x(), getter="get"):
    """Get all modules from a path (see get_modules), call a function
    in each of them and return its results. The getter function is 'get' by wstbot convention
    and the results are usually objects, therefore the name of this function.

    f will be used to call the getter function.

    If there is no getter function, look for a CLASS_ variable and try
    to instantiate it using f."""

    results = []
    modules = get_modules(path)
    for module in modules:
        # try to call the getter function
        func = getattr(module, getter, None)
        if func is not None:
            results.append(f(func))
        else:
            # try to instantiate the class
            class_ = getattr(module, "CLASS_", None)
            if class_ is not None:
                results.append(f(class_))
            else:
                logger.info("Omitting {0}.".format(module.__name__))

    return results

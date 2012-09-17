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

import os

class Logger:
    """Simple logging class"""

    def __init__(self, *outputs):
        self.outputs = None
        self.prefix = ""
        self.enabled = True
        if outputs is not None and len(outputs) > 0:
            self.outputs = outputs

    def add_output(self, output):
        if output is not None:
            # check for write method
            try:
                output.write
                self.outputs.append(output)
            except NameError:
                print("Output handler has no write method!")

    def write(self, message):
        if not self.enabled:
            return

        for output in self.outputs:
            output.write(self.prefix + " " + message)

    def info(self, message):
        self.write(message)

    def warn(self, message):
        self.write("WARNING: " + message)

    def error(self, message):
        self.write("ERROR: " + message)

    def recv(self, message):
        self.write("<- " + message)

    def send(self, message):
        self.write("-> " + message)

    def debug(self, message):
        self.write("DEBUG: " + message)

    def close(self):
        for output in self.outputs:
            try:
                output.close()
            except NameError:
                pass

class Printer(object):

    def write(self, message):
        print(message)

class FileWriter(object):

    def __init__(self, filename):
        self.fp = open(filename, "w")

    def write(self, message):
        self.fp.write(message + os.linesep)

    def close(self, message):
        self.fp.close()

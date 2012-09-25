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
import time
import re
import shutil
from wstbot_locals import DATA_PATH, BACKUP_PATH
from botserver.util import get_template_content

ENCODING = "utf-8"

# regex constants
REGEX_FILE_NAME = "regex.yaml"
REGEX_FILE_PATH = os.path.join(DATA_PATH, REGEX_FILE_NAME)
REGEX_BACKUP_PATH = os.path.join(BACKUP_PATH, "regex")

class RegexUpdater:
    """Updates the regex info for regex retrieval"""

    NEEDLE = "{regexdata}"
    
    def update(self, regexdata):
        if regexdata is None:
            print("New regex data was None!")

        self.backup_regex()

        # write new regex
        fp = open(REGEX_FILE_PATH, "wb")
        fp.write(regexdata.encode("utf-8"))
        fp.close()

        return "New regex file was written."

    def backup_regex(self):
        if not os.path.exists(REGEX_FILE_PATH):
            print("No previous regex data, nothing to back up!")
            return

        # make a backup
        try:
            os.mkdir(BACKUP_PATH)
        except os.error:
            pass

        shutil.copyfile(REGEX_FILE_PATH, os.path.join(REGEX_BACKUP_PATH, REGEX_FILE_NAME + str(time.time())))

    def make_page(self, template):
        if not os.path.exists(REGEX_FILE_PATH):
            return template.replace(self.NEEDLE, "")
        else:
            fp = open(REGEX_FILE_PATH, "rb")
            content = fp.read()
            fp.close()
            content = content.decode(ENCODING)
            return template.replace(self.NEEDLE, content)

def access(regex=None):
    updater = RegexUpdater()
    if regex is None:
        return updater.make_page(get_template_content("regex.html"))
    else:
        return updater.update(regex)

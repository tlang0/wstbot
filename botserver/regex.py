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

ENCODING = "utf-8"

# regex constants
REGEX_FILE = os.path.join("data", "regex.yaml")
REGEX_BACKUP_DIR = "regexbackups"
REGEX_BACKUP_PATH = os.path.join("botserver", REGEX_BACKUP_DIR)

class RegexUpdater:
    """Updates the regex info for regex retrieval"""

    NEEDLE = "{regexdata}"
    
    def update(self, regexdata):
        if regexdata is None:
            print("New regex data was None!")

        if not os.path.exists(REGEX_FILE):
            print("No previous regex data!")
        else:
            # backup old regex file
            if not os.path.exists(REGEX_BACKUP_PATH):
                os.mkdir(REGEX_BACKUP_PATH)

            shutil.copyfile(REGEX_FILE, os.path.join(REGEX_BACKUP_PATH, REGEX_FILE + str(time.time())))

        # write new regex
        fp = open(REGEX_FILE, "wb")
        fp.write(regexdata.encode("utf-8"))
        fp.close()

        return "New regex file was written."

    def make_page(self, template):
        if not os.path.exists(REGEX_FILE):
            return template.replace(self.NEEDLE, "")
        else:
            fp = open(REGEX_FILE, "rb")
            content = fp.read()
            fp.close()
            content = content.decode(ENCODING)
            return template.replace(self.NEEDLE, content)



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
from string import Template

ENCODING = "utf-8"

# siteinfo constants
SITEINFO_FILE_NAME = "siteinfo.yaml"
SITEINFO_FILE_PATH = os.path.join(DATA_PATH, SITEINFO_FILE_NAME)
SITEINFO_BACKUP_PATH = os.path.join(BACKUP_PATH, "siteinfo")

class SiteinfoUpdater:
    """Updates the siteinfo info for info retrieval"""

    def __init__(self, html_template):
        self.html_template = html_template

    def index(self, siteinfo=None):
        return self.make_page(self.html_template)
    
    def update(self, infodata):
        if infodata is None:
            print("New info data was None!")

        self.backup_siteinfo()

        # write new data
        fp = open(SITEINFO_FILE_PATH, "wb")
        fp.write(infodata.encode("utf-8"))
        fp.close()

        return "New siteinfo file was written."

    def backup_siteinfo(self):
        if not os.path.exists(SITEINFO_FILE_PATH):
            print("No previous siteinfo data, nothing to back up!")
            return

        # make a backup
        try:
            os.mkdir(BACKUP_PATH)
        except os.error:
            pass

        try:
            os.mkdir(SITEINFO_BACKUP_PATH)
        except os.error:
            pass

        shutil.copyfile(SITEINFO_FILE_PATH, os.path.join(SITEINFO_BACKUP_PATH, SITEINFO_FILE_NAME + str(time.time())))

    def make_page(self, html_template):
        template = Template(html_template)
        content = ""
        if os.path.exists(SITEINFO_FILE_PATH):
            with open(SITEINFO_FILE_PATH, "rb") as fp:
                content = fp.read()
            content = content.decode(ENCODING)

        new_html = template.substitute(infodata=content)
        return new_html

    index.exposed = True
    update.exposed = True

def get():
    updater = SiteinfoUpdater(get_template_content("siteinfo.html"))
    return updater

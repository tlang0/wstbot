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

# converts media files to an sqlite db
# will _not_ be updated anymore

import sqlite3
import os
import json
from util import str_list_to_int

MEDIA_PATH = os.path.join("data", "media")
MEDIA_DB_PATH = os.path.join("data", "media.db")

def main():
    filelist = os.listdir(MEDIA_PATH)

    if filelist is None or (len(filelist)) <= 0:
        print("no files found")
        return

    filelist_int = str_list_to_int(filelist)
    filelist = [str(x) for x in sorted(filelist_int)]

    with sqlite3.connect(MEDIA_DB_PATH) as conn:
        cur = conn.cursor()
        for filename in filelist:
            with open(os.path.join(MEDIA_PATH, filename), "r") as mfile:
                for line in mfile.readlines():
                    data = json.loads(line)
                    if type(data) != dict:
                        continue
                    if "title" not in data:
                        data["title"] = ""
                    cur.execute("insert into media (type, title, url) values (?, ?, ?)",
                            (data["type"], data["title"], data["url"]))
        conn.commit()

if __name__ == "__main__":
    main()

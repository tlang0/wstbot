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

# -*- coding: utf-8 -*-

import os
import re
import urllib.request
from util import str_list_to_int

WEB_ENCODING = "utf-8"

class Image:

    SERVER_IMAGES_PATH = os.path.join("botserver", "images")
    
    def __init__(self):
        if not os.path.exists(self.SERVER_IMAGES_PATH):
            print("Path does not exist: " + os.path.abspath(self.SERVER_IMAGES_PATH))
            self.working = False
            return

        self.working = True
        filelist = os.listdir(self.SERVER_IMAGES_PATH) 
        filelist_int = str_list_to_int(filelist)
        filelist = [str(x) for x in sorted(filelist_int)]
        if len(filelist) <= 0:
            new_file_name = "1"
        else:
            new_file_name = str(int(filelist[-1]) + 1)

        print("New image file: {0}".format(new_file_name))
        self.filepath = os.path.join(self.SERVER_IMAGES_PATH, new_file_name)
        self.num_imagelinks = 0
    
    def imgur(self, url):
        print("imgur link")
        content = urllib.request.urlopen(url).read().decode(WEB_ENCODING)
        match1 = re.search('<a href="(.*)" target="_blank">View full resolution', content)
        match2 = re.search('<link rel="image_src" href="(.*)"\s*/>', content)
        match = match1 or match2
        if match:
            print("imgur match")
            imageurl = match.groups()[0]
            if imageurl:
                return imageurl
        else:
            return None
        
    def parse(self, bot, msg, nick):
        if not self.working or msg[-1] == "*":
            return
        
        # prefix for URLs in general
        prefix = "(https?://)(www\.)?"
        imgurmatch = re.search(".*(" + prefix + "imgur.com/(.*/)?((\d|\w)*)(/)?)", msg)
        match = re.search(".*(" + prefix + ".*(\.jpeg|\.jpg|\.png|\.gif))", msg)
        if imgurmatch:
            url = self.imgur(imgurmatch.groups()[0])
        elif match:
            url = match.groups()[0]
        else:
            return
        if url == None:
            return
        
        print("Found image url: " + url)
        fp = open(self.filepath, "a")
        fp.write(url + os.linesep)
        fp.close()
        self.num_imagelinks += 1
        
        if self.num_imagelinks % 10 == 0 and self.num_imagelinks != 0:
            return str(self.num_imagelinks) + " pictures! "

    def close(self):
        self.fp.close()

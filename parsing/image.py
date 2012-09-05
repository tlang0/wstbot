# -*- coding: utf-8 -*-

import os
import re
import urllib2

class Image(object):

    SERVER_IMAGES_PATH = os.path.join("botserver", "images")
    
    def __init__(self):
        if not os.path.exists(self.SERVER_IMAGES_PATH):
            print("Path does not exist: " + os.path.abspath(self.SERVER_IMAGES_PATH))
            self.working = False
            return

        self.working = True
        filelist = os.listdir(self.SERVER_IMAGES_PATH) 
        filelist.sort()
        if len(filelist) <= 0:
            new_file_name = "1"
        else:
            new_file_name = str(int(filelist[-1]) + 1)

        print("New image file: " + str(new_file_name))
        self.filepath = os.path.join(self.SERVER_IMAGES_PATH, new_file_name)
        self.num_imagelinks = 0
    
    def imgur(self, url):
        print("imgur link")
        content = urllib2.urlopen(url).read()
        #match = re.search('<a href="(.*)" target="_blank">View full resolution', content)
        match = re.search('<link rel="image_src" href="(.*)"\s*/>', content)
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
        
        imgurmatch = re.search("((https?://)(www\.)?imgur.com/((\d|\w)*)(/)?)", msg)
        match = re.search("((http://|www\.).*(\.jpeg|\.jpg|\.png|\.gif))", msg)
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

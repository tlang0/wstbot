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

# -*- coding: utf-8 -*-

import re
import os
import urllib.request
from commands.command import Command

WEB_ENCODING = "utf-8"
FORTUNEDISABLED = "This category is currently disabled."

class Fortune(Command):
    
    def do(self, argstr, nick):
        if self.silent:
            return
        
        message = ""
        
        while True:
            self.logger.info("Trying to get fortune message..")
            
            if argstr.strip() != "":
                message = self.fortune(argstr)
            else:
                message = self.fortune()
                
            # don't accept fortunes that are too long
            if message and message.count('\n') > 5 or message == None:
                continue
            else:
                break
                          
        return message
    
    # replace special characters
    def handle_html(self, text):
        text = text.replace('&#39;', '\'')
        text = text.replace('&amp;', '&')
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&quot;', '"')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&auml;', 'ä')
        text = text.replace('&ouml;', 'ö')
        text = text.replace('&uuml;', 'ü')
        text = text.replace('&Auml;', 'Ä')
        text = text.replace('&Ouml;', 'Ö')
        text = text.replace('&Uuml;', 'Ü')
        
        return text
        
    # schneier facts
    def get_schneier(self):
        site = urllib.request.urlopen("http://www.schneierfacts.com/").read().decode(WEB_ENCODING)
        match = re.search(r'<p class="fact">(.*?)</p>', site, re.DOTALL)
        if match:
            fact = match.groups()[0]
            if fact:
                fact = self.handle_html(fact)
                return fact
        else:
            return "Could not retrieve a schneier fact."
            
    # get fortune
    def fortune(self, category=None, maxlength=None):
        if self.silent:
            return None
        
        args = ""

        if maxlength:
            args += " -s " #-n " + str(maxlength)
        else:
            args += " -s " #-n " + str(300) # max 400 zeichen
            
        if category:
            if category.find(' ') != -1:
                return
            category = category.strip()
            
            if category == "schneier":
                return self.get_schneier()
            elif category == "ascii-art":
                return FORTUNEDISABLED
#            elif category == "list":
#                return FORTUNELIST
            else:
                args += " " + category
        
        try:
            return os.popen("fortune" + args).read()
        except:
            return

    def get_cmd(self):
        return "fortune"

    def get_help(self):
        return "Get a random fortune or a schneier fact with '!fortune schneier'"

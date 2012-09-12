# -*- coding: utf-8 -*-

import urllib2, re, os
from command import Command

FORTUNEDISABLED = "This category is currently disabled."

class Fortune(Command):
    
    def __init__(self):
        self.silent = False

    def do(self, bot, argstr, nick):
        if self.silent:
            return
        
        message = ""
        
        while True:
            bot.log.info("Trying to get fortune message..")
            
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
        site = urllib2.urlopen("http://www.schneierfacts.com/").read()
        match = re.search(r'<p class="fact">(.*?)</p>', site, re.DOTALL)
        if match:
            fact = match.groups()[0]
            if fact:
                print fact
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

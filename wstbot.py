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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import wirc
import os
import importlib
import botlog
import configparser
from colors import C
from util import apply_seq

##### DIRECTORIES / FILE PATHS #####

COMMANDS_DIR = "commands"
PARSING_DIR = "parsing"
FILE_LOG = "wstbot.log"

###### ERROR MESSAGES ######

DEFAULTERROR = "An error occurred!"

##### MESSAGES ######

QUITMSG = "bye."
HELPMSG = 'Type !help to see a list of commands.'
HELLOMSG = 'Hello, #CHANNEL! ' + HELPMSG
WELCOMEMSG = 'Hello, #NICK!'
FORTUNEMSG = "Your fortune for today is:\n#FORTUNE"
NO_HELP_MSG = "There is no help message for this command!"

def module_exists(module_name):
    try:
        importlib.import_module(module_name)
    except:
        return False
    else:
        return True

class WstBotLoader:

    def load(self, debug=False):
        parser = configparser.SafeConfigParser()
        parser.read("wstbot.conf")

        server = parser.get("connection_data", "server")
        port = int(parser.get("connection_data", "port"))
        nick = parser.get("connection_data", "nick")
        snick = parser.get("connection_data", "snick")
        ident = parser.get("connection_data", "ident")
        realname = parser.get("connection_data", "realname")
        channel = parser.get("connection_data", "channel")
        wstbot_server_port = int(parser.get("server_config", "port"))

        return WstBot(server, nick, port, ident, realname, channel, server_port=wstbot_server_port, debug=debug)

class WstBot(wirc.wIRC):

    def __init__(self, server, nick, port, ident, realname, channel, 
            server_port=8111, debug=False):
        wirc.wIRC.__init__(self, server, nick, port, ident, realname, debug)
        self.silent = False

        # initialize logger
        self.log = botlog.Logger(botlog.Printer(), botlog.FileWriter(FILE_LOG))
        self.log.default_prefix = "WSTBOT"
        self.chan = channel
        self.commands = self.objects_from_files(COMMANDS_DIR)
        self.keywords = self.objects_from_files(PARSING_DIR)
        self.server_port = server_port

    def objects_from_files(self, directory):
        """
        1. Read files from a folder
        2. Create objects from the classes contained in the files which should
           have the same name as the file, with the first letter in upper case

        """
        
        objects = []

        # Load object objects
        for objectfile in os.listdir(directory):
            if objectfile[-2:] != "py" or objectfile[0] in [".", "_"]:
                continue

            objectclass = objectfile[0].upper() + objectfile[1:objectfile.rfind('.')]
            objectmodule = objectclass.lower()

            # omit templates (abstract classes)
            if objectmodule == "command" or objectmodule == "parser":
                continue

            try:
                self.log.info("Importing object '" + objectclass + "'...")
                module = importlib.import_module("{0}.{1}".format(directory, objectmodule))
                class_ = getattr(module, objectclass)
                obj = class_(self)
                objects.append(obj)
            except ImportError as err:
                self.log.warn("Importing '{0}' from '{1}' was unsuccessful!".format(objectclass, objectfile))
                self.log.warn("Reason: {}".format(err))

        return objects

    # Send a formatted message
    def formatted_msg(self, chan, msg, addcolor=True):
        def sendline(line):
            if line != "": # ignore empty lines
                if addcolor:
                    self.msg(chan, C.NORMAL + line)
                else:
                    self.msg(chan, line)
                
        if msg:
            lines = msg.split("\n")
            apply_seq(sendline, lines)
                    
    # Send a message to the current channel
    def chanmsg(self, msg, addcolor=True):
        self.formatted_msg(self.chan, msg, addcolor)

    def get_command_object(self, cmd):
        if cmd.strip() == "":
            return None
        for cmd_obj in self.commands:
            if cmd == cmd_obj.get_cmd():
                return cmd_obj
        return None

    # Handle privmsg
    def on_privmsg(self, nick, ident, server, target, msg):    
        # parsing. accept direct messages too
        if msg is None:
            self.log.warn("on_privmsg: msg was None")
        if msg == "":
            self.log.warn("on_privmsg: msg was empty")
        if msg[0] != "!":
            # check for keywords
            for cmd_obj in self.keywords:
                self.chanmsg(cmd_obj.do_parse(msg, nick))

            return

        # don't accept whispered and very short commands
        if target != self.chan or len(msg) <= 2:
            return

        firstword = msg
        argstr = "" # string with arguments
        # if message contains more than one word
        if " " in msg:
            firstword = msg[:msg.find(" ")]
            argstr = msg[msg.find(" ")+1:]
        # user command
        ucmd = firstword[1:]
        # empty command?
        if ucmd.strip() == "":
            return
        
        # !help command
        if firstword == "!help":
            # try to get help for a specific command
            if " " in msg:
                cmd_obj = self.get_command_object(msg.split()[1])
                if cmd_obj:
                    help_msg = cmd_obj.get_help()
                    if help_msg is not None and help_msg.strip() != "":
                        self.chanmsg(help_msg)
                    else:
                        self.chanmsg(NO_HELP_MSG)
                        
            # general help
            else:
                cmds = ""
                for cmd in self.commands:
                    cmds += "!" + cmd.get_cmd() + ", "
                self.chanmsg("Commands: " + cmds[:-2])
                self.chanmsg("Also try !help [command] (without !)")
        else:
            # check for command
            cmd_obj = self.get_command_object(ucmd)
            if cmd_obj:
                self.chanmsg(cmd_obj.do_cmd(argstr, nick))

    # Joining a channel
    def on_me_join(self, channel):
        hello_msg = HELLOMSG.replace('#CHANNEL', channel)
        self.chanmsg(hello_msg)
        
    # Someone else joins a channel
    def on_join(self, nick, ident, server):
        welcome_msg = WELCOMEMSG.replace("#NICK", nick)
        fortune_cmd_obj = self.get_command_object("fortune")
        if fortune_cmd_obj:
            fortune = fortune_cmd_obj.do_cmd("", nick)
            welcome_msg += " " + FORTUNEMSG.replace("#FORTUNE", fortune)
        self.chanmsg(welcome_msg)
        
    # Handle all received data
    def on_receive(self, line):
        # This could be quakenet specific
        if "End of" in line and "376" in line:
            self.join(self.chan)

    def provide_special_options(self):
        print("Commands: msg, join")
        try:
            command = input()
            sp = command.find(" ")
            c = command[:sp]
            argstr = command[sp + 1:]

            if c == "msg":
                self.chanmsg(argstr)
            elif c == "join":
                self.part(self.chan)
                self.join(argstr)
                self.chan = argstr
        except KeyboardInterrupt:
            return -1

if __name__ == '__main__':
    wstbot = WstBotLoader().load(debug=True)
    wstbot.connect()

    while True:
        try:
            wstbot.doirc()
        except KeyboardInterrupt:
            o = wstbot.provide_special_options()
            if o == -1:
                wstbot.log.info("bye!")
                wstbot.log.close()
                wstbot.quit()
                break

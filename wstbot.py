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

import os
import importlib
import configparser
import logging
from util import apply_seq
from wstbot_locals import STREAM_LOG_FORMAT, FILE_LOG_FORMAT

##### DIRECTORIES / FILE PATHS #####

COMMANDS_DIR = "commands"
PARSING_DIR = "parsing"
FILE_LOG = "wstbot.log"

###### ERROR MESSAGES ######

DEFAULTERROR = "An error occurred!"

##### MESSAGES ######

QUITMSG = "bye."
HELPMSG = 'Type !help to see a list of commands.'
HELLOMSG = 'Hello, {channel}! ' + HELPMSG
WELCOMEMSG = 'Hello, {nick}!'
FORTUNEMSG = "Your fortune for today is:\n{fortune}"
NO_HELP_MSG = "There is no help message for this command!"

logger = logging.getLogger(__name__)
logger.propagate = False

class WstBot:

    def __init__(self, transport, debug=False):
        # initialize logger
        if debug:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        self.transport = transport

        # stream handler
        stream_handler = logging.StreamHandler()
        stream_formatter = logging.Formatter(STREAM_LOG_FORMAT)
        stream_handler.setFormatter(stream_formatter)
        # file handler
        file_handler = logging.FileHandler(FILE_LOG)
        file_formatter = logging.Formatter(FILE_LOG_FORMAT)
        file_handler.setFormatter(file_formatter)
        # add handlers
        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

        # load modules
        self.commands = self.objects_from_files(COMMANDS_DIR)
        self.keywords = self.objects_from_files(PARSING_DIR)

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
                logger.info("Importing object '" + objectclass + "'...")
                module = importlib.import_module("{0}.{1}".format(directory, objectmodule))
                class_ = getattr(module, objectclass)
                obj = class_(self, logger)
                objects.append(obj)
            except ImportError as err:
                logger.warning("Importing '{0}' from '{1}' was unsuccessful!".format(objectclass, objectfile))
                logger.warning("Reason: {}".format(err))

        return objects

    def get_command_object(self, cmd):
        if cmd.strip() == "":
            return None
        for cmd_obj in self.commands:
            if cmd == cmd_obj.get_cmd():
                return cmd_obj
        return None

    def handle_message(self, nick, msg):    
        # parsing. accept direct messages too
        if msg is None:
            logger.warning("msg was None")
        if msg == "":
            logger.warning("msg was empty")
        if msg[0] != "!":
            # check for keywords
            for cmd_obj in self.keywords:
                self.send_room_message(cmd_obj.do_parse(msg, nick))
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
                        self.send_room_message(help_msg)
                    else:
                        self.send_room_message(NO_HELP_MSG)
                        
            # general help
            else:
                cmds = ""
                for cmd in self.commands:
                    cmds += "!" + cmd.get_cmd() + ", "
                self.send_room_message("Commands: " + cmds[:-2])
                self.send_room_message("Also try !help [command] (without !)")
        else:
            # check for command
            cmd_obj = self.get_command_object(ucmd)
            if cmd_obj:
                self.send_room_message(cmd_obj.do_cmd(argstr, nick))

    def send_room_message(self, msg):
        self.transport.send_room_message(msg)

    def on_me_join(self, channel):
        hello_msg = HELLOMSG.format(channel=channel)
        self.send_room_message(hello_msg)
        
    def on_join(self, nick):
        welcome_msg = WELCOMEMSG.format(nick=nick)
        fortune_cmd_obj = self.get_command_object("fortune")
        if fortune_cmd_obj:
            fortune = fortune_cmd_obj.do_cmd("", nick)
            welcome_msg += " " + FORTUNEMSG.format(fortune=fortune)
        self.send_room_message(welcome_msg)
        
    # Handle all received data
    def on_receive(self, line):
        # This could be quakenet specific
        if "End of" in line and "376" in line:
            self.join(self.chan)


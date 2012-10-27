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
import configparser
import logging
from colors import IRCFormats
from util import apply_seq
from wstbot_locals import STREAM_LOG_FORMAT, FILE_LOG_FORMAT
from wstbot import WstBot

logger = logging.getLogger(__name__)

def wstbot_load(debug=False):
    parser = configparser.SafeConfigParser()
    parser.read("wstbot.conf")
    
    category = "irc_connection"

    server = parser.get(category, "server")
    port = int(parser.get(category, "port"))
    nick = parser.get(category, "nick")
    snick = parser.get(category, "snick")
    ident = parser.get(category, "ident")
    realname = parser.get(category, "realname")
    channel = parser.get(category, "channel")

    return WstBotIRC(server, nick, port, ident, realname, channel, debug)

class WstBotIRC(wirc.wIRC):

    def __init__(self, server, nick, port, ident, realname, channel, debug=False):
        super().__init__(server, nick, port, ident, realname, debug=debug)
        self.silent = False
        self.chan = channel
        self.msg_formats = IRCFormats()
        self.wstbot = WstBot(self, debug=True)

    # Send a formatted message
    def formatted_msg(self, chan, msg, addcolor=True):
        def sendline(line):
            if line != "": # ignore empty lines
                if addcolor:
                    self.msg(chan, self.msg_formats.default_color(line))
                else:
                    self.msg(chan, line)
                
        if msg:
            lines = msg.split("\n")
            apply_seq(sendline, lines)
                    
    # Send a message to the current channel
    def chanmsg(self, msg, addcolor=True):
        self.formatted_msg(self.chan, msg, addcolor)

    def send_room_message(self, message, formatted=True):
        # there is no real difference between formatted and unformatted messages in irc
        self.chanmsg(message)
    
    # Handle privmsg
    def on_privmsg(self, nick, ident, server, target, msg):    
        self.wstbot.handle_message(nick, msg)

    # Joining a channel
    def on_me_join(self, channel):
        self.wstbot.on_me_join(channel)
        
    # Someone else joins a channel
    def on_join(self, nick, ident, server):
        self.wstbot.on_join(nick)
        
    # Handle all received data
    def on_receive(self, line):
        # This could be quakenet specific
        if "End of" in line and "376" in line:
            self.join(self.chan)

    def cli_options(self):
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
            return None

if __name__ == '__main__':
    bot = wstbot_load(debug=True)
    bot.connect()

    while True:
        try:
            bot.doirc()
        except KeyboardInterrupt:
            o = bot.cli_options()
            if o is None:
                bot.quit()
                break

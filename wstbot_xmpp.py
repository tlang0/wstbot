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

import logging
import configparser
from w_xmpp import WstXMPP
from wstbot import WstBot
from wstbot_locals import STREAM_LOG_FORMAT
from colors import XMPPFormats

# these settings will be used by sleekxmpp
logging.basicConfig(level=logging.INFO, format=STREAM_LOG_FORMAT)

def wstbot_load(debug=False):
    parser = configparser.SafeConfigParser()
    parser.read("wstbot.conf")
    
    category = "xmpp_connection"

    account = parser.get(category, "account")
    password = parser.get(category, "password")
    room = parser.get(category, "room")
    nick = parser.get(category, "nick")

    return WstBotXMPP(account, password, room, nick)

class WstBotXMPP(WstXMPP):

    def __init__(self, *args):
        super().__init__(*args)

        self.msg_formats = XMPPFormats()
        self.wstbot = WstBot(self, debug=True)

    def muc_message(self, msg):
        # ignore messages from self
        if msg["mucnick"] == self.nick:
            return

        self.wstbot.handle_message(msg["from"].user, msg["body"])

    def muc_online(self, presence):
        # ignore own status changes
        if presence["muc"]["nick"] == self.nick:
            return

        #self.send_message(mto=presence["from"].bare, mbody="hi", mtype="groupchat")

    def send_room_message(self, message):
        self.send_message(mto=self.room, mbody=message, mtype="groupchat")

if __name__ == "__main__":
    bot = wstbot_load()

    if bot.connect():
        bot.process(block=True)
    else:
        logging.error("Unable to connect")

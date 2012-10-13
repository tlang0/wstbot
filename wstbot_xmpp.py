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
from w_xmpp import WstXMPP
#from wstbot import WstBot

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def wstbot_load():
    return WstBotXMPP("wstbot@dukgo.com", "aq1sw2", "hibforumtest@conference.dukgo.com", "wstbot")

class WstBotXMPP(WstXMPP):

    def __init__(self, *args):
        super().__init__(*args)

#        self.wstbot = WstBot(self, debug=True)

    def muc_message(self, msg):
        # ignore messages from self
        if msg["mucnick"] == self.nick:
            return

        response = self.wstbot.handle_message(msg["body"], msg["from"].user)
        logger.debug(response)
        self.send_message(mto=msg["from"].bare, mbody=response, mtype="groupchat")

    def muc_online(self, presence):
        # ignore own status changes
        if presence["muc"]["nick"] == self.nick:
            return

        self.send_message(mto=presence["from"].bare, mbody="hi", mtype="groupchat")

if __name__ == "__main__":
    logger.debug("start")
    bot = wstbot_load()

    if bot.connect():
        bot.process(block=True)
    else:
        logger.error("Unable to connect")

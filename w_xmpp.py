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

import sys
import logging
import getpass
import sleekxmpp
from optparse import OptionParser

logger = logging.getLogger(__name__)

class WstXMPP(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password, room, nick):
        super().__init__(jid, password)

        self.room = room
        self.nick = nick

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("groupchat_message", self.muc_message)
        self.add_event_handler("muc::{0}::got_online".format(self.room), self.muc_online)

        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0045') # Multi-User Chat
        self.MUC = self.plugin['xep_0045']
        self.register_plugin('xep_0199') # XMPP Ping

    def start(self, event):
        self.get_roster()
        self.send_presence()

        self.MUC.joinMUC(self.room, self.nick, wait=True)

    def muc_message(self, msg):
        pass

    def muc_online(self, presence):
        pass

if __name__ == "__main__":
    bot = WstXMPP("wstbot@dukgo.com", "aq1sw2", "hibforum@conference.dukgo.com", "wstbot")
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)-8s %(message)s")
    if bot.connect():
        bot.process(block=True)
    else:
        print("unable to connect")

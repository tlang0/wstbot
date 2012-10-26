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

import os
import subprocess
import cherrypy
import time
import configparser
from string import Template
from botserver.util import get_template_content

PORT = 8112
SLEEP_AMOUNT = 3

class ControlInterface:

    def __init__(self):
        self.wstbot_xmpp_proc = None
        self.wstbot_irc_proc = None
        self.wstbot_server_proc = None

    @cherrypy.expose
    def index(self, bot_xmpp_button=False, bot_irc_button=False, server_button=False):

        # start or stop processes

        if bot_xmpp_button:
            self.start_stop_wstbot_xmpp()
        elif bot_irc_button:
            self.start_stop_wstbot_irc()
        elif server_button:
            self.start_stop_server()

        # show page
        template = Template(get_template_content("controlinterface.html"))
        # xmpp text
        bot_xmpp_button_text = "Start XMPP Wstbot"
        if self.process_running(self.wstbot_xmpp_proc):
            bot_xmpp_button_text = "Stop XMPP Wstbot"
        # irc text
        bot_irc_button_text = "Start IRC Wstbot"
        if self.process_running(self.wstbot_irc_proc):
            bot_irc_button_text = "Stop IRC Wstbot"
        # server text
        server_button_text = "Start Wstbot Server"
        if self.process_running(self.wstbot_server_proc):
            server_button_text = "Stop Wstbot Server"
        # format
        page = template.substitute(bot_xmpp_button_text=bot_xmpp_button_text,
                                   bot_irc_button_text=bot_irc_button_text, 
                                   server_button_text=server_button_text)
        return page

    def process_running(self, proc):
        if proc is not None:
            proc.poll()
            if proc.returncode is not None:
                return False
            else:
                return True
        else:
            return False

    def start_stop_process(self, proc, start):
        if self.process_running(proc):
            proc.terminate()
            return None
        else:
            return start()

    def start_stop_wstbot_xmpp(self):
        self.wstbot_xmpp_proc = self.start_stop_process(self.wstbot_xmpp_proc, 
                lambda : subprocess.Popen(["python3", "-m", "wstbot_xmpp"]))
        time.sleep(SLEEP_AMOUNT)
        
    def start_stop_wstbot_irc(self):
        self.wstbot_irc_proc = self.start_stop_process(self.wstbot_irc_proc,
                lambda : subprocess.Popen(["python3", "-m", "wstbot_irc"]))
        time.sleep(SLEEP_AMOUNT)

    def start_stop_server(self):
        self.wstbot_server_proc = self.start_stop_process(self.wstbot_server_proc,
                lambda : subprocess.Popen(["python3", "-m", "botserver.server"]))
        time.sleep(SLEEP_AMOUNT)

def main():
    # load config
    parser = configparser.SafeConfigParser()
    parser.read("wstbot.conf")
    category = "control_interface"
    port = parser.get(category, "port")
    port = int(port)

    # apply config
    cherrypy.config.update({
        "server.socket_port": port,
        "server.socket_host": "0.0.0.0"
    })

    # start server
    server = ControlInterface()
    cherrypy.tree.mount(server, "/")
    cherrypy.engine.start()
    cherrypy.engine.block()
        
if __name__ == "__main__":
    main()

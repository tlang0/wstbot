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

import configparser
from botserver import cherryserver

class Server:

    def __init__(self, port):
        self.dependency = "cherrypy"
        self.port = port
        
    def start(self):
        cherryserver.start(self.port)

def load_server():
    parser = configparser.SafeConfigParser()
    parser.read("wstbot.conf")
    category = "server_config"
    port = parser.get(category, "port")
    return Server(int(port))

if __name__ == "__main__":
    server = load_server()
    server.start()

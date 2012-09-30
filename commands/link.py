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
from commands.command import Command

class Link(Command):

    DEFAULT = "/media"

    def do(self, argstr, nick):
        parser = configparser.SafeConfigParser()
        parser.read("wstbot.conf")
        address = parser.get("server_config", "address")
        port = parser.get("server_config", "port")
        web_interface_port = parser.get("control_interface", "port")
        server_url = address + ":" + port

        argstr = argstr.strip()
        if argstr == "media":
            return server_url + "/media"
        elif argstr == "regex" or argstr == "news":
            return server_url + "/regex"
        elif argstr == "interface":
            return address + ":" + web_interface_port
        else:
            return server_url + self.DEFAULT
    
    def get_cmd(self):
        return "link"

    def get_help(self):
        return "Get the link to something on the server. \nOptions: media, news, interface. Default: " + self.DEFAULT

CLASS_ = Link

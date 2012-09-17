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

from commands.command import Command

class Youtubefrontend(Command):

    def do(self, bot, argstr, nick):
        argstr = argstr.strip()

        if not " " in argstr:
            return

        spc = argstr.find(" ")
        user = argstr[:spc]
        option = argstr[spc + 1:]

        if option == "viewcount":
            option = "viewCount"

        return "http://gdata.youtube.com/feeds/api/users/{0}/uploads?orderby={1}".format(user, option)

    def get_cmd(self):
        return "youtube"

    def get_help(self):
        return """!youtube <user> <option>\n<user>: The user account\n
<option>: One of: relevance, published, viewCount, rating"""

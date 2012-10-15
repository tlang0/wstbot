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

import random
from commands.command import Command

class Lmgtfy(Command):

    def do(self, argstr, nick):
        if (argstr.strip() != ""):
            return "http://lmgtfy.com/?q={0}".format(argstr.replace(" ", "+").strip())

    def get_cmd(self):
        return "lmgtfy"

    def get_help(self):
        return "!lmgtfy <term>\nLet me google that for you. "

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
import logging
from commands.command import Command

logger = logging.getLogger("wstbot")

class Roll(Command):

    def do(self, argstr, nick):
        maxroll = 100
            
        if argstr.strip() != "":
            try:
                maxroll = int(argstr.strip())
            except:
                logger.warning("rolling: given argument is not an integer")
               
        if maxroll > 0:
            try:
                roll = random.choice(range(maxroll))
                return nick + " rolls " + str(roll) + " (0-" + str(maxroll) + ")"
            except:
                logger.error("roll error!")

    def get_cmd(self):
        return "roll"

    def get_help(self):
        return "!roll [limit]\nGenerate a random integer in the interval [0,limit]. " \
            + "By default, limit is 100."

CLASS_ = Roll

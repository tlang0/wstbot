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

###### IRC COLORS / FORMATTING ######

#~ IRC Colors according to:
#~ http://www.mirc.com/help/colors.html
#~ 0 white
#~ 1 black
#~ 2 blue (navy)
#~ 3 green
#~ 4 red
#~ 5 brown (maroon)
#~ 6 purple
#~ 7 orange (olive)
#~ 8 yellow
#~ 9 light green (lime)
#~ 10 teal (a green/blue cyan)
#~ 11 light cyan (cyan) (aqua)
#~ 12 light blue (royal)
#~ 13 pink (light purple) (fuchsia)
#~ 14 grey
#~ 15 light grey (silver)

class C:
    NOFO = chr(15) # not bold, not italic
    NORMAL = chr(3) + "14" # standard color for messages

    BLACK = chr(3) + "01"
    BLUE = chr(3) + "02"
    GREEN = chr(3) + "03"
    RED = chr(3) + "04"
    #BROWN = chr(3) + "05"
    PURPLE = chr(3) + "06"
    BOLD = chr(2)

colors = {"default": C.NORMAL, "black": C.BLACK, "blue": C.BLUE, "green": C.GREEN, 
        "red": C.RED, "purple": C.PURPLE}
styles = {"default": C.NOFO, "bold": C.BOLD}

class Formats:

    def get(self, format_name, message):
        return getattr(self, format_name)(message)

class IRCFormats(Formats):

    def black(self, message):
        return C.BLACK + message + C.NORMAL

    def blue(self, message):
        return C.BLUE + message + C.NORMAL

    def green(self, message):
        return C.GREEN + message + C.NORMAL

    def red(self, message):
        return C.RED + message + C.NORMAL

    def purple(self, message):
        return C.PURPLE + message + C.NORMAL

    def bold(self, message):
        return C.BOLD + message + C.NOFO

class XMPPFormats(Formats):

    def __getattr__(self, name):
        return self.format

    def format(self, message):
        return message

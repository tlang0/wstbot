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

class C(object):
    NOFO = chr(15) # not bold, not italic
    NORMAL = chr(3) + "14" # standard color for messages

    BLACK = chr(3) + "01"
    BLUE = chr(3) + "02"
    GREEN = chr(3) + "03"
    RED = chr(3) + "04"
    #BROWN = chr(3) + "05"
    VIOLET = chr(3) + "06"
    BOLD = chr(2)

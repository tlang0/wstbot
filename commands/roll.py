import random

class Roll(object):

    def do(self, bot, argstr, nick):
        """
        Execute the command.

        Arguments:
        bot -- instance of WstBot
        argstr -- argument string (for "!cmd a b c", argstr would be "a b c")
        nick -- nickname of the person who sent the command

        """

        maxroll = 100
            
        if argstr.strip() != "":
            try:
                maxroll = int(argstr.strip())
            except:
                print "rolling: given argument is not an integer"
               
        if maxroll > 0:
            try:
                roll = random.choice(range(maxroll))
                bot.chanmsg(nick + ' rolls ' + str(roll) + ' (0-' + str(maxroll) + ')')
            except:
                print "roll error"


    def get_cmd(self):
        """ Return the raw command """
        return "roll"

    def get_help(self):
        """ Return help for this specific command """
        return "!roll [limit]\nGenerate a random integer in the interval [0,limit]. " \
            + "By default, limit is 100."
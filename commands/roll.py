import random
from commands.command import Command

class Roll(Command):

    def do(self, bot, argstr, nick):
        maxroll = 100
            
        if argstr.strip() != "":
            try:
                maxroll = int(argstr.strip())
            except:
                bot.log.warn("rolling: given argument is not an integer")
               
        if maxroll > 0:
            try:
                roll = random.choice(range(maxroll))
                bot.chanmsg(nick + ' rolls ' + str(roll) + ' (0-' + str(maxroll) + ')')
            except:
                bot.log.error("roll error!")


    def get_cmd(self):
        return "roll"

    def get_help(self):
        return "!roll [limit]\nGenerate a random integer in the interval [0,limit]. " \
            + "By default, limit is 100."

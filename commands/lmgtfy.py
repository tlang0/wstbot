import random
from commands.command import Command

class Lmgtfy(Command):

    def do(self, bot, argstr, nick):
        if (argstr.strip() != ""):
            bot.chanmsg("http://lmgtfy.com/?q={0}".format(argstr.replace(" ", "+").strip()))

    def get_cmd(self):
        return "lmgtfy"

    def get_help(self):
        return "!lmgtfy <term>\nLet me google that for you. "

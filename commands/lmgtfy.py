import random

class Lmgtfy(object):

    def do(self, bot, argstr, nick):
        """
        Execute the command.

        Arguments:
        bot -- instance of WstBot
        argstr -- argument string (for "!cmd a b c", argstr would be "a b c")
        nick -- nickname of the person who sent the command

        """

        if (argstr.strip() != ""):
            bot.chanmsg("http://lmgtfy.com/?q={0}".format(argstr.replace(" ", "+").strip()))

    def get_cmd(self):
        """ Return the raw command """
        return "lmgtfy"

    def get_help(self):
        """ Return help for this specific command """
        return "!lmgtfy <term>\nLet me google that for you. "

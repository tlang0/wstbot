import socket

class About(object):

    def do(self, bot, argstr, nick):
        """
        Execute the command.

        Arguments:
        bot -- instance of WstBot
        argstr -- argument string (for "!cmd a b c", argstr would be "a b c")
        nick -- nickname of the person who sent the command

        """

        try:
            return "Running on " + socket.gethostname()
        except:
            return "An error occurred."

    def get_cmd(self):
        """ Return the raw command """
        return "about"

    def get_help(self):
        """ Return help for this specific command """
        return "Information about the computer the bot is running on."

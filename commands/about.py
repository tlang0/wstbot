import socket
from command import Command

class About(Command):

    def do(self, bot, argstr, nick):
        try:
            return "Running on " + socket.gethostname()
        except:
            return "An error occurred."

    def get_cmd(self):
        return "about"

    def get_help(self):
        return "Information about the computer the bot is running on."

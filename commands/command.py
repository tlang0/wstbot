class Command:
    """A template for commands"""

    def __init__(self):
        self.disabled = False

    def do(self, bot, argstr, nick):
        """
        Execute the command.

        Arguments:
        bot -- instance of WstBot
        argstr -- argument string (for "!cmd a b c", argstr would be "a b c")
        nick -- nickname of the person who sent the command

        The return string will be sent to the active channel.

        """
        
        return ""
        
    def get_cmd(self):
        """ Return the raw command """
        return ""

    def get_help(self):
        """ Return help for this specific command """
        return ""

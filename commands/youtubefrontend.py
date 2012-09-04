class Youtubefrontend(object):

    def do(self, bot, argstr, nick):
        """
        Execute the command.

        Arguments:
        bot -- instance of WstBot
        argstr -- argument string (for "!cmd a b c", argstr would be "a b c")
        nick -- nickname of the person who sent the command

        """

        argstr = argstr.strip()

        if not " " in argstr:
            return

        spc = argstr.find(" ")
        user = argstr[:spc]
        option = argstr[spc + 1:]

        if option == "viewcount":
            option = "viewCount"

        return "http://gdata.youtube.com/feeds/api/users/{0}/uploads?orderby={1}".format(user, option)

        bot.chanmsg("http://lmgtfy.com/?q={0}".format(argstr.replace(" ", "+").strip()))

    def get_cmd(self):
        """ Return the raw command """
        return "youtube"

    def get_help(self):
        """ Return help for this specific command """
        return """!youtube <user> <option>\n<user>: The user account\n
<option>: One of: relevance, published, viewCount, rating"""

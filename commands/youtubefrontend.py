from commands.command import Command

class Youtubefrontend(Command):

    def do(self, bot, argstr, nick):
        argstr = argstr.strip()

        if not " " in argstr:
            return

        spc = argstr.find(" ")
        user = argstr[:spc]
        option = argstr[spc + 1:]

        if option == "viewcount":
            option = "viewCount"

        return "http://gdata.youtube.com/feeds/api/users/{0}/uploads?orderby={1}".format(user, option)

    def get_cmd(self):
        return "youtube"

    def get_help(self):
        return """!youtube <user> <option>\n<user>: The user account\n
<option>: One of: relevance, published, viewCount, rating"""

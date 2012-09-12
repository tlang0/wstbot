import configparser
from commands.command import Command

class Link(Command):

    DEFAULT = "/images"

    def do(self, bot, argstr, nick):
        parser = configparser.SafeConfigParser()
        parser.read("wstbot.conf")
        address = parser.get("server_config", "address")
        port = parser.get("server_config", "port")
        server_url = address + ":" + port

        argstr = argstr.strip()
        if argstr == "images":
            return server_url + "/images"
        elif argstr == "regex" or argstr == "news":
            return server_url + "/regex"
        else:
            return server_url + self.DEFAULT
    
    def get_cmd(self):
        return "link"

    def get_help(self):
        return "Get the link to something on the server. Options: images, news. Default: " + self.DEFAULT

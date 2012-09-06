import ConfigParser
from command import Command

class Link(Command):

    def do(self, bot, argstr, nick):
        parser = ConfigParser.SafeConfigParser()
        parser.read("wstbot.conf")
        address = parser.get("server_config", "address")
        port = parser.get("server_config", "port")
        return address + ":" + port + "/images"
    
    def get_cmd(self):
        return "link"

    def get_help(self):
        return "Link to the image collection"

import ConfigParser

class Link(object):

    def do(self, bot, argstr, nick):
        parser = ConfigParser.SafeConfigParser()
        parser.read("wstbot.conf")
        address = parser.get("server_config", "address")
        return address + "/images"
    
    def get_cmd(self):
        return "link"

    def get_help(self):
        return "Link to the image collection"

import os
import cherrypy
import time
import shutil
from botserver.regex import RegexUpdater
from botserver.images import ImageListBuilder

# server constants
SERVER_CONFIG_PATH = os.path.join("botserver", "cherryserver.conf")

# image constants
TEMPLATES_PATH = os.path.join("botserver", "templates")

class CherryServer:

    def index(self):
        return self.get_template("index.html")
        
    def images(self, page=None):
        builder = ImageListBuilder() 
        return builder.build(self.get_template("images.html"), page)

    def regex(self, regex=None):
        updater = RegexUpdater()
        if regex is None:
            return updater.make_page(self.get_template("regex.html"))
        else:
            return updater.update(regex)

    def style(self):
        return self.get_template("style.css")

    def get_template(self, name):
        try:
            path = os.path.join(TEMPLATES_PATH, name)
            fp = open(path, "r")
            content = fp.read()
            fp.close()
            return content
        except IOError:
            return "File not found: " + name

    index.exposed = True
    images.exposed = True
    regex.exposed = True
    style.exposed = True

def start(port):
    cherrypy.config.update({
        "server.socket_port": port,
        "server.socket_host": "0.0.0.0"
    })
    app_path = os.path.dirname(os.path.abspath(__file__))
    config = {
        "/style.css":
        {
            "tools.staticfile.on": True,
            "tools.staticfile.filename": os.path.join(app_path, "templates/style.css")
        }
    }
    cherrypy.tree.mount(CherryServer(), "/", config=config)
    cherrypy.engine.start()
    cherrypy.engine.block()

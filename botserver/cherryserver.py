########################################################################
# Copyright 2012 wst, wstcode@gmail.com
#
# This file is part of wstbot.
#
# wstbot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wstbot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with wstbot.  If not, see <http://www.gnu.org/licenses/>.
########################################################################

import os
import cherrypy
import time
import shutil
from botserver.regex import RegexUpdater
from botserver.media import MediaListBuilder

# server constants
SERVER_CONFIG_PATH = os.path.join("botserver", "cherryserver.conf")
TEMPLATES_PATH = os.path.join("botserver", "templates")

class CherryServer:

    def index(self):
        return self.get_template("index.html")
        
    def media(self, page=None):
        builder = MediaListBuilder() 
        return builder.build(self.get_template("media.html"), page)

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
    media.exposed = True
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

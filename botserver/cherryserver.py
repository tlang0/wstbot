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
import yaml
import importlib
from wstbot_locals import DESCRIPTION_PATH 
from botserver.util import get_template_content

def load_modules_description():
    fp = open(DESCRIPTION_PATH, "r")
    modules_data = yaml.safe_load(fp)
    fp.close()
    return modules_data

class CherryServer:

    def __init__(self, modules_data):
        self.modules_data = modules_data

    @cherrypy.expose
    def index(self):
        return get_template_content("index.html")

    def load_modules(self):
        """Dynamically load server modules using the description file"""
        if "modules" not in self.modules_data:
            print("modules not found in modules.yaml")
            return
        
        for module_data in self.modules_data["modules"]:
            name = module_data["name"]
            module = importlib.import_module("botserver.modules." + name)
            # enable web access
            setattr(self, name, module.access)
            getattr(self, name).exposed = True

def make_config(modules_data):
    if "static_templates" not in modules_data:
        print("static_templates not found in modules.yaml")

    app_path = os.path.dirname(os.path.abspath(__file__))
    config = {}

    # get a list of the file names
    names = [template_data["name"] for template_data in modules_data["static_templates"]]

    for name in names:
        config["/" + name] = {
            "tools.staticfile.on": True,
            "tools.staticfile.filename": os.path.join(app_path, "templates/" + name)
        }

    return config

def start(port):
    modules_data = load_modules_description()
    cherrypy.config.update({
        "server.socket_port": port,
        "server.socket_host": "0.0.0.0"
    })
    config = make_config(modules_data)
    server = CherryServer(modules_data)
    server.load_modules()
    cherrypy.tree.mount(server, "/", config=config)
    cherrypy.engine.start()
    cherrypy.engine.block()

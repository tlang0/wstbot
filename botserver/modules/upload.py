########################################################################
# Copyright 2012 honboubao, ctsaplg@wolke7.net
#
# This file is part of wstbot.
#
# wstbot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wstbot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with wstbot. If not, see <http://www.gnu.org/licenses/>.
########################################################################

import os
import cherrypy
import mimetypes
import string
import random
from urllib.parse import quote_plus
from urllib.parse import unquote_plus
from botserver.util import get_template_content
from string import Template
from cherrypy.lib.static import serve_file
from cgi import escape

DEFAULT_FILE = "upload.html"
localDir = os.path.dirname(__file__)
absDir = os.path.join(os.getcwd(), localDir)
dir = "files"

class Uploader:
    """File upload page"""
    
    @cherrypy.expose
    def index(self):
        html_template = get_template_content(DEFAULT_FILE)
        template = Template(html_template)        
        return template.substitute(actionUrl=(self.get_request_url() + "submit"))
        
    @cherrypy.expose
    def submit(self, file):
        url = self.get_request_url()
        url = url[0:url.find("submit")]
        
        filename = quote_plus(file.filename)
        id = ""
        # if the plain filename is already in use we generate an id with at least 6 characters
        while os.path.isfile(os.path.join(absDir, dir, filename)) and len(id) < 6 or os.path.isfile(os.path.join(absDir, dir, id + "_" + filename)):
            id += random.choice(string.ascii_letters)
        savedFile = open(os.path.join(absDir, dir, (id + "_" if id else "") + filename), "wb")
        while True:
            data = file.file.read(8192)
            if not data:
                break          
            savedFile.write(data)
        savedFile.close()
        
        if id:
          filename = id + "/" + filename
        out = "<div class='entry'>"
        if (file.content_type.value.find("image") > -1): 
            out +="<img src='" + url + "show/" + filename + "'>"            
        out += "<label>"+ escape(file.filename) +"</label><br>\
                File link: <a href='" + url + "show/" + filename + "'>" + url + "show/" + filename + "</a><br>\
                Download link: <a href='" + url + "download/" + filename + "'>" + url + "download/" + filename + "</a><br>\
                Delete link: <a href='" + url + "delete/" + filename + "'>" + url + "delete/" + filename + "</a>\
                </div>"
        return out
        
    @cherrypy.expose
    def show(self, id, filename=None):
        if not filename:
          filename = id
        else:
          filename = id + "_" + filename
        return self.serve_file(filename, False)
        
    @cherrypy.expose
    def download(self, id, filename=None):
        if not filename:
          filename = id
        else:
          filename = id + "_" + filename
        return self.serve_file(filename, True)
        
    @cherrypy.expose
    def delete(self, id, filename=None):
        if not filename:
          filename = id
        else:
          filename = id + "_" + filename
        path = os.path.join(absDir, dir, filename)
        try:
            os.remove(path)
        except os.error as e:
            return "Error: File not found. %s" % e
        return "File succesfully deleted."
        
    def get_request_url(self):
        base = cherrypy.request.base
        path = cherrypy.request.path_info
        if not path.endswith("/"):
            path = path + "/"
        return base + path
    
    
    def serve_file(self, filename, download=False):
        disposition = None
        path = os.path.join(absDir, dir, filename)
        mime =  mimetypes.guess_type(filename)[0]
        if (not mime): 
            mime = "application/octet-stream"
        orgfilename = unquote_plus(filename[filename.find("_") + 1:])
        if (download):
            disposition = "attachment"
        try:
            return serve_file(path, mime, disposition, orgfilename, True)
        except cherrypy.NotFound as e:
            return "Error: File not found."
        
def get():
    builder = Uploader()
    return builder
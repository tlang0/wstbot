import os
import cherrypy

SERVER_PATH = "botserver"
TEMPLATES_PATH = os.path.join(SERVER_PATH, "templates")

class ImageListBuilder(object):
    """Build a html image list from json image files containing lists of image URLs.
    In the html template, #{images} will be replaced by the list"""

    IMAGES_DIR = os.path.join(SERVER_PATH, "images")

    def build(self, template):
        filelist = os.listdir(self.IMAGES_DIR) 
        if len(filelist) <= 0: 
            print("No image files found!")
        
        path_list = os.path.join(self.IMAGES_DIR, filelist[-1])
        fp = open(path_list, "r")
        image_list = fp.readlines()

        images_html = ""
        for url in image_list:
            if url[-1] == os.linesep:
                url = url[:-1]
            images_html += '<p><img src="{0}" alt="Some image" /></p>\n'.format(url)
            images_html += "<hr />\n"

        fp.close()

        return template.replace("{{images}}", images_html)

class CherryServer(object):

    def index(self):
        return self.get_template("index.html")
        
    def images(self):
        builder = ImageListBuilder() 
        return builder.build(self.get_template("images.html"))

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

def start(port):
    cherrypy.config.update({"server.socket_port": port})
    cherrypy.quickstart(CherryServer())

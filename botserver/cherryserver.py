import os
import cherrypy

SERVER_PATH = "botserver"
TEMPLATES_PATH = os.path.join(SERVER_PATH, "templates")

class ImageListBuilder(object):
    """Build a html image list from json image files containing lists of image URLs.
    In the html template, #{images} will be replaced by the list"""

    IMAGES_DIR = os.path.join(SERVER_PATH, "images")

    def build(self, template, page=None):
        filelist = os.listdir(self.IMAGES_DIR) 
        images_html = ""

        # no images
        if len(filelist) <= 0: 
            print("No image files found!")
            images_html = "No images yet!"
        else:
            if page is not None and page in filelist:
                shown_page = page
            else:
                shown_page = filelist[-1]

            pos_in_list = filelist.index(shown_page)

            path_list = os.path.join(self.IMAGES_DIR, shown_page)
            fp = open(path_list, "r")
            image_list = fp.readlines()

            # insert links to previous and next page
            images_html += "<p>\n"
            if pos_in_list > 0:
                images_html += '''<a href="/images/{0}" title="previous page"><- previous page
                    </a>&nbsp;\n'''.format(filelist[pos_in_list - 1])
            if pos_in_list < len(filelist) - 1:
                images_html += '''<a href="/images/{0}" title="next page">next page ->
                    </a>\n'''.format(filelist[pos_in_list + 1])
            images_html += "</p>\n"

            # insert images
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
        
    def images(self, page=None):
        builder = ImageListBuilder() 
        return builder.build(self.get_template("images.html"), page)

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

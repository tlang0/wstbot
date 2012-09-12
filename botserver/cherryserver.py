import os
import cherrypy
import time
import shutil

# server constants
SERVER_PATH = "botserver"
SERVER_CONFIG_PATH = os.path.join(SERVER_PATH, "cherryserver.conf")

# image constants
TEMPLATES_PATH = os.path.join(SERVER_PATH, "templates")

# news constants
REGEX_FILE = "REGEX"
REGEX_BACKUP_DIR = "regexbackups"
REGEX_BACKUP_PATH = os.path.join(SERVER_PATH, REGEX_BACKUP_DIR)

class ImageListBuilder(object):
    """Build a html image list from files containing the image URLs.
    In the html template, {{images}} will be replaced by the list"""

    IMAGES_DIR = os.path.join(SERVER_PATH, "images")

    def build(self, template, page=None):
        filelist = os.listdir(self.IMAGES_DIR) 
        images_html = ""

        # no images
        if len(filelist) <= 0: 
            print("No image files found!")
            images_html = "No images yet!"
        else:
            # sort
            filelist_int = [int(x) for x in filelist]
            filelist = [str(x) for x in sorted(filelist_int)]

            if page is not None and page in filelist:
                shown_page = page
            else:
                shown_page = filelist[-1]

            pos_in_list = filelist.index(shown_page)

            path_list = os.path.join(self.IMAGES_DIR, shown_page)
            fp = open(path_list, "r")
            image_list = fp.readlines()

            # insert links to previous and next page
            prev_html=""
            next_html=""
            if pos_in_list > 0:
                prev_html += ('<a href="/images/{0}" title="previous page">&lt;- previous page'
                    + '</a>&nbsp;\n').format(filelist[pos_in_list - 1])
            if pos_in_list < len(filelist) - 1:
                next_html += ('<a href="/images/{0}" title="next page">next page -&gt;'
                    + '</a>\n').format(filelist[pos_in_list + 1])
            template = template.replace("{navprev}", prev_html)
            template = template.replace("{navnext}", next_html)

            # insert images
            i = 0
            for url in image_list:
                if url[-1] == os.linesep:
                    url = url[:-1]
                images_html += '<p><img src="{0}" alt="Some image" /></p>\n'.format(url)
                i += 1
                if i < len(image_list):
                  images_html += "<hr />\n"

            fp.close()

        return template.replace("{images}", images_html)

class NewsUpdater(object):
    """Updates the regex info for news headline retrieval"""

    NEEDLE = "{regexdata}"
    
    def update(self, regexdata):
        if regexdata is None:
            print("New regex data was None!")

        if not os.path.exists(REGEX_FILE):
            print("No previous regex data!")
        else:
            # backup old regex file
            if not os.path.exists(REGEX_BACKUP_PATH):
                os.mkdir(REGEX_BACKUP_PATH)

            shutil.copyfile(REGEX_FILE, os.path.join(REGEX_BACKUP_PATH, REGEX_FILE + str(time.time())))

        # write new regex
        fp = open(REGEX_FILE, "wb")
        fp.write(regexdata.encode("utf-8"))
        fp.close()

        return "New news file was written."

    def make_page(self, template):
        if not os.path.exists(REGEX_FILE):
            return template.replace(self.NEEDLE, "")
        else:
            fp = open(REGEX_FILE, "rb")
            content = fp.read()
            fp.close()
            return template.replace(self.NEEDLE, content)

class CherryServer(object):

    def index(self):
        return self.get_template("index.html")
        
    def images(self, page=None):
        builder = ImageListBuilder() 
        return builder.build(self.get_template("images.html"), page)

    def news(self, newsregex=None):
        updater = NewsUpdater()
        if newsregex is None:
            return updater.make_page(self.get_template("news.html"))
        else:
            return updater.update(newsregex)

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
    news.exposed = True
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

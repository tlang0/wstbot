import os
from wstbot_locals import TEMPLATES_PATH

def get_template_content(name):
    try:
        path = os.path.join(TEMPLATES_PATH, name)
        fp = open(path, "r")
        content = fp.read()
        fp.close()
        return content
    except IOError:
        return "File not found: " + name


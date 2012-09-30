import re
from wstbot_locals import URL_REGEX_PREFIX
from parsing.parser import Parser

OH_NO = "Your Jabber client doesn't show images. Change that."

class ImageDisplay(Parser):
    
    def parse(self, msg, nick):
        img_url_match = re.search(URL_REGEX_PREFIX + "\S+\.(png|jpg|jpeg|gif)", msg)
        if img_url_match:
            img_url = img_url_match.group(0)
            return '<img src="{0}" alt="{1}" />'.format(img_url, OH_NO)

CLASS_ = ImageDisplay

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
import json
from util import str_list_to_int
from wstbot_locals import DATA_PATH, TEMPLATES_PATH
from botserver.util import get_template_content
from string import Template

# places newer entries on top if true
MEDIA_PATH = os.path.join(DATA_PATH, "media")

class MediaListBuilder:
    """Build an html media list from files containing the media URLs.
    In the html template, ${media} will be replaced by the list"""

    def __init__(self, html_template):
        self.html_template = html_template

    def index(self, page=None, ascending=False):
        try:
            ascending = bool(int(ascending))
        except:
            ascending = False
        filelist = os.listdir(MEDIA_PATH) 
        htmldata = ""

        template = Template(self.html_template)

        # no media
        if len(filelist) <= 0: 
            print("No media files found!")
            return "No media yet!"

        # sort
        filelist_int = str_list_to_int(filelist)
        filelist = [str(x) for x in sorted(filelist_int)]

        # determine page
        if page is not None and page in filelist:
            shown_page = page
        else:
            shown_page = filelist[-1]

        pos_in_list = filelist.index(shown_page)
        path_list = os.path.join(MEDIA_PATH, shown_page)

        def build_link(page):
            # copy the current get variables but use a different page number
            link = "/media?page=" + str(page)
            if ascending:
                link += "&ascending=" + str(int(ascending))
            return link

        def build_navigation_link(nav):
            # nav is a positive or negative number
            list_index = (pos_in_list + nav) % len(filelist)
            return build_link(filelist[list_index])

        # read the media links and construct the page
        with open(path_list, "r") as fp:
            media_list = fp.readlines()
            media_iter = iter(media_list) if ascending == True else reversed(media_list)

            # insert links to previous and next page
            prev_html=""
            next_html=""
            if pos_in_list > 0:
                prev_html += ('<a href="{0}" title="previous page">&lt;- previous page'
                    + '</a>&nbsp;\n').format(build_navigation_link(-1))
            if pos_in_list < len(filelist) - 1:
                next_html += ('<a href="{0}" title="next page">next page -&gt;'
                    + '</a>\n').format(build_navigation_link(1))

            # insert media
            for i, media_info_json in enumerate(media_iter):
                # media_info should be a dict, in some versions it could be a list
                media_info = json.loads(media_info_json)
                media_info = self.media_info_to_dict(media_info)
                htmldata += self.get_html(media_info)
                if i < len(media_list):
                    htmldata += "<hr />\n"

        new_html = template.substitute(
                navprev=prev_html,
                navnext=next_html,
                media=htmldata)

        return new_html

    def media_info_to_dict(self, x):
        if type(x) == list:
            return {"type": x[0], "url": x[1]}
        return x

    def get_html(self, media_info):
        """media_info should be a dict"""
        url = media_info["url"]
        if url[-1] == os.linesep:
            url = url[:-1]
        type_ = media_info["type"]
        # start constructing the output
        html_str = "<p>"
        title = ""
        if "title" in media_info:
            title = media_info["title"]
        # add the actual content
        if type_ == "link":
            if title == "":
                title = url
            html_str += '<a href="{0}" title="{1}">{1}</a>'.format(url, title)
        elif type_ == "image":
            html_str += '<img src="{0}" alt="{1}" title={2} />'.format(url, title, title)
        elif type_ == "youtube":
            if title != "":
                html_str += "<div><strong>" + title + "</strong></div>\n"
            html_str += ('<iframe width="560" height="315" src="http://www.youtube.com/embed/{0}" ' \
                    + 'frameborder="0" title="{1}" allowfullscreen></iframe>').format(url, title)
        else:
            return 'corrupted data'

        html_str += "</p>\n"
        return html_str

    index.exposed = True

def access():
    builder = MediaListBuilder(get_template_content("media.html"))
    return builder

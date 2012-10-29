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
import sqlite3
import cherrypy
from util import str_list_to_int
from wstbot_locals import DATA_PATH, TEMPLATES_PATH
from botserver.util import get_template_content
from string import Template

# places newer entries on top if true
MEDIA_DB_PATH = os.path.join(DATA_PATH, "media.db")
DEFAULT_FILE = "media.html"
NOJS_FILE = "media-nojs.html"
ITEMS_PER_PAGE = 15

class MediaListBuilder:
    """Build an html media list from the media database.
    In the html template, ${media} will be replaced by the contents"""

    def __init__(self):
        self.nr = 1

    @cherrypy.expose
    def load(self, nr=1, ascending=False):
        """Return items starting at nr"""

        self.nr = nr
        htmldata = ""
        order = "asc" if ascending else "desc"

        # get the media data and construct the page
        with sqlite3.connect(MEDIA_DB_PATH) as conn:
            # make items accessible by name
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("select * from media order by id " + order + " limit ?, ?", 
                    (nr, ITEMS_PER_PAGE))

            # insert media
            for row in cur:
                htmldata += self.make_content_html(row)
                htmldata += "<hr />\n"

        return htmldata

    @cherrypy.expose
    def index(self, nr=1, ascending=False):
        html_template = get_template_content(DEFAULT_FILE)
        template = Template(html_template)
        
        htmldata = self.load(nr, ascending)
        new_html = template.substitute(media=htmldata, nr=self.nr)

        return new_html

    @cherrypy.expose
    def nojs(self, nr=1):
        if nr != 1:
            nr = int(nr)
        htmldata = ""
        html_template = get_template_content(NOJS_FILE)
        template = Template(html_template)
       
        def build_link(sign):
            # copy the current get variables but use a different page number
            link = "/media/nojs?nr=" + str(nr + sign * ITEMS_PER_PAGE)
            return link

        # insert links to previous and next page
        prev_html = ('<a href="{0}" title="previous page">&lt;- previous page'
                + '</a>&nbsp;\n').format(build_link(1))
        if nr <= ITEMS_PER_PAGE:
            next_html = ""
        else:
            next_html = ('<a href="{0}" title="next page">next page -&gt;'
                + '</a>\n').format(build_link(-1))
        
        htmldata = "<ul>\n" + self.load(nr) + "\n</ul>"

        new_html = template.substitute(
                navprev=prev_html,
                navnext=next_html,
                media=htmldata)

        return new_html

    def make_content_html(self, row):
        """row should be a dict"""
        url = row["url"]
        if url[-1] == os.linesep:
            url = url[:-1]
        type_ = row["type"]
        # start constructing the output
        html_str = "<li>"
        title = ""
        if "title" in row:
            title = row["title"]
        # add the actual content
        if type_ == "link":
            if title == "":
                title = url
            html_str += '<a href="{0}" title="{1}">{1}</a>'.format(url, title)
        elif type_ == "image":
            html_str += '<img src="{0}" alt="{1}" title={2} />'.format(url, title, title)
        elif type_ == "youtube":
            if title != "":
                html_str += '<div class="item-title">{0}</div>\n'.format(title)
            html_str += ('<iframe width="720" height="405" src="http://www.youtube.com/embed/{0}" ' \
                    + 'frameborder="0" title="{1}" allowfullscreen></iframe>').format(url, title)
        else:
            return 'corrupted data'

        html_str += "</li>\n"
        return html_str

def access():
    builder = MediaListBuilder()
    return builder

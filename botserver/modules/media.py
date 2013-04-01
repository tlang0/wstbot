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
import shutil
import time
import logging
from wstbot_locals import DATA_PATH, TEMPLATES_PATH, BACKUP_PATH
from botserver.util import get_template_content
from string import Template

YOUTUBE_VIDEO_HTML = ('<iframe width="720" height="405" src="http://www.youtube.com/embed/{0}" '
                    + 'frameborder="0" title="{1}" allowfullscreen></iframe>')
VIMEO_VIDEO_HTML = ('<iframe src="http://player.vimeo.com/video/{0}" width="720" height="405" '
                    + 'frameborder="0" title="{1}" webkitAllowFullScreen mozallowfullscreen '
                    + 'allowFullScreen></iframe>')

# places newer entries on top if true
MEDIA_DB_PATH = os.path.join(DATA_PATH, "media.db")
BACKUP_DB_PATH = os.path.join(BACKUP_PATH, "media")
DEFAULT_FILE = "media.html"
NOJS_FILE = "media-nojs.html"
ITEMS_PER_PAGE = 15

logger = logging.getLogger("server")

class MediaListBuilder:
    """Build an html media list from the media database.
    In the html template, ${media} will be replaced by the contents"""

    def __init__(self):
        self.nr = 0
        self.is_search = False

    @cherrypy.expose
    def load(self, nr=0, ascending=False, search=None):
        """Return items starting at nr"""

        self.nr = nr
        htmldata = ""
        order = "asc" if ascending else "desc"

        # get the media data and construct the page
        with sqlite3.connect(MEDIA_DB_PATH) as conn:
            cur = conn.cursor()
            if search is not None:
                if search.text == "":
                    return "Empty search!"
                # filter on title and url
                qry = ("select * from media where title like '%' || ? || '%' or url like '%' "
                    + "|| ? || '%' order by id " + order)
                data = (search.text, search.text)
            else:
                qry = "select * from media order by id " + order + " limit ?, ?"
                data = (nr, ITEMS_PER_PAGE)
            cur.execute(qry, data)

            # insert media
            for row in cur:
                htmldata += self.make_content_html(id=row[0], type=row[1], title=row[2], url=row[3])
                htmldata += "<hr />\n"

        return htmldata

    @cherrypy.expose
    def index(self, nr=0, ascending=False, search_text=None, filter_on=None):
        html_template = get_template_content(DEFAULT_FILE)
        template = Template(html_template)

        self.is_search = False if search_text is None else True
        search = None
        if search_text is not None:
            search = Search(search_text, filter_on)
        
        htmldata = self.load(nr, ascending=ascending, search=search)
        new_html = template.substitute(media=htmldata, nr=self.nr, search=self.is_search)

        return new_html

    @cherrypy.expose
    def nojs(self, nr=0):
        if nr != 0:
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

    def backup_db(self):
        """Make a backup of the database"""

        try:
            os.mkdir(BACKUP_PATH)
        except os.error as e:
            logger.error(e)

        try:
            os.mkdir(BACKUP_DB_PATH)
        except os.error as e:
            logger.error(e)

        shutil.copyfile(MEDIA_DB_PATH, os.path.join(BACKUP_DB_PATH, "media.db." + str(time.time())))

    @cherrypy.expose
    def delete(self, id_):
        # backup db
        try:
            self.backup_db()
        except:
            logger.error("DB Backup failed (delete)!")
            return ""

        # delete item with id_
        with sqlite3.connect(MEDIA_DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("delete from media where id = ?", (id_,))

        return id_

    def make_content_html(self, **row):
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

        # replace double quotes
        title = title.replace("\"", "&quot;")

        # add the actual content
        if type_ == "link":
            if title == "":
                title = url
            html_str += '<a href="{0}" title="{1}">{1}</a>'.format(url, title)
        elif type_ == "image":
            html_str += '<img src="{0}" alt="{1}" title="{2}" />'.format(url, title, title)
        elif title != "":
            if type_ == "youtube":
                html_str += '<div class="item-title"><a href="http://www.youtube.com/watch?v={0}">{1}</a></div>\n'.format(url, title)
                html_str += YOUTUBE_VIDEO_HTML.format(url, title)
            elif type_ == "vimeo":
                html_str += '<div class="item-title"><a href="{0}">{1}</a></div>\n'.format(url, title)
                html_str += VIMEO_VIDEO_HTML.format(url, title)
        else:
            return "Invalid type!\n"

        html_str += "\n"

        # add delete link
        html_str += ('<a href="javascript:void(0);" title="delete" class="delete-button" id="{0}">' \
                + '<img src="/img/delete.png" alt="delete" /></a>\n').format(row["id"])

        html_str += "</li>\n"
        return html_str

class Search:

    def __init__(self, text, filter_on):
        self.text = text
        self.filter_on = filter_on

def get():
    builder = MediaListBuilder()
    return builder

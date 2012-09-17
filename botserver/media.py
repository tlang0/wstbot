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

# places newer entries on top if true
SHOW_DESCENDING = True
MEDIA_PATH = os.path.join("data", "media")

class MediaListBuilder:
    """Build an html media list from files containing the media URLs.
    In the html template, {media} will be replaced by the list"""

    def build(self, template, page=None):
        filelist = os.listdir(MEDIA_PATH) 
        htmldata = ""

        # no media
        if len(filelist) <= 0: 
            print("No media files found!")
            htmldata = "No media yet!"
        else:
            # sort
            filelist_int = str_list_to_int(filelist)
            filelist = [str(x) for x in sorted(filelist_int)]

            if page is not None and page in filelist:
                shown_page = page
            else:
                shown_page = filelist[-1]

            pos_in_list = filelist.index(shown_page)

            path_list = os.path.join(MEDIA_PATH, shown_page)
            fp = open(path_list, "r")
            media_list = fp.readlines()
            media_iter = reversed(media_list) if SHOW_DESCENDING else iter(media_list)

            # insert links to previous and next page
            prev_html=""
            next_html=""
            if pos_in_list > 0:
                prev_html += ('<a href="/media/{0}" title="previous page">&lt;- previous page'
                    + '</a>&nbsp;\n').format(filelist[pos_in_list - 1])
            if pos_in_list < len(filelist) - 1:
                next_html += ('<a href="/media/{0}" title="next page">next page -&gt;'
                    + '</a>\n').format(filelist[pos_in_list + 1])
            template = template.replace("{navprev}", prev_html)
            template = template.replace("{navnext}", next_html)

            # insert media
            for i, media_info_json in enumerate(media_iter):
                media_info = json.loads(media_info_json)
                htmldata += self.get_html(media_info)
                if i < len(media_list):
                    htmldata += "<hr />\n"

            fp.close()

        return template.replace("{media}", htmldata)

    def get_html(self, media_info):
        url = media_info[1]
        if url[-1] == os.linesep:
            url = url[:-1]
        type_ = media_info[0]
        if type_ == "link":
            return '<p><a href="{0}" title="Some link">{0}</a></p>\n'.format(url)
        elif type_ == "image":
            return '<p><img src="{0}" alt="Some image" /></p>\n'.format(url)
        elif type_ == "youtube":
            return ('<p><iframe width="560" height="315" src="http://www.youtube.com/embed/{0}" ' \
                    + 'frameborder="0" allowfullscreen></iframe>').format(url)
        else:
            return 'corrupted data'



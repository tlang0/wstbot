import os
from util import str_list_to_int

# places newer entries on top if true
SHOW_DESCENDING = True

class ImageListBuilder:
    """Build a html image list from files containing the image URLs.
    In the html template, {{images}} will be replaced by the list"""

    IMAGES_DIR = os.path.join("botserver", "images")

    def build(self, template, page=None):
        filelist = os.listdir(self.IMAGES_DIR) 
        images_html = ""

        # no images
        if len(filelist) <= 0: 
            print("No image files found!")
            images_html = "No images yet!"
        else:
            # sort
            filelist_int = str_list_to_int(filelist)
            filelist = [str(x) for x in sorted(filelist_int)]

            if page is not None and page in filelist:
                shown_page = page
            else:
                shown_page = filelist[-1]

            pos_in_list = filelist.index(shown_page)

            path_list = os.path.join(self.IMAGES_DIR, shown_page)
            fp = open(path_list, "r")
            image_list = fp.readlines()
            image_iter = reversed(image_list) if SHOW_DESCENDING else iter(image_list)

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
            for url in image_iter:
                if url[-1] == os.linesep:
                    url = url[:-1]
                images_html += '<p><img src="{0}" alt="Some image" /></p>\n'.format(url)
                i += 1
                if i < len(image_list):
                  images_html += "<hr />\n"

            fp.close()

        return template.replace("{images}", images_html)



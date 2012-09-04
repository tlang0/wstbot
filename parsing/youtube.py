# -*- coding: utf-8 -*-

import re, gdata.youtube, gdata.youtube.service
from colors import C

YTERROR = "An error occured while retrieving information about the youtube video."
YOUTUBEMSG = C.RED + "#POS" + C.BOLD + C.VIOLET \
        + "#TITLE" + C.NOFO + C.BLACK + " :: " + C.GREEN + "#DURATION"

class Youtube(object):

    def parse(self, bot, msg, nick):
        if msg[-1] == "*":
            return
        if not ("youtube." in msg and "v=" in msg) and not ("youtu.be") in msg:
            return

        # video id
        match = re.search('v=(.*?)(&.*?)?$', msg)
        match2 = re.search("be/(.*)", msg)
        print msg
        if match or match2:
            if match:
                url_id = match.groups()[0]
            elif match2:
                url_id = match2.groups()[0]
            print url_id
            
            try:
                # google/youtube api
                ytclient = gdata.youtube.service.YouTubeService()
                video = ytclient.GetYouTubeVideoEntry(video_id=url_id)
                if video:
                    # position
                    match = re.search('(&|#)t=(.*?)(&.*?)?$', msg)
                    if match:
                        pos = match.groups()[1]
                    else:
                        pos = None
                    
                    # infos
                    duration = int(video.media.duration.seconds)
                    durationstr = str(duration/60) + "m " + str(duration%60) + "s"
                    title = video.media.title.text
                    ratingstr = video.rating.average + " (" + video.rating.num_raters + " votes)"
                    youtubestr = YOUTUBEMSG
                    youtubestr = youtubestr.replace("#TITLE", title)
                    youtubestr = youtubestr.replace("#DURATION", durationstr)
                    youtubestr = youtubestr.replace("#RATING", ratingstr)
                    if pos:
                        youtubestr = youtubestr.replace("#POS", "(AT: %s) " % (pos))
                    else:
                        youtubestr = youtubestr.replace("#POS", "")
                    return youtubestr
            except:
                print YTERROR
              

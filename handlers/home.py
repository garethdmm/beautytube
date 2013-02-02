import tornado.auth
import tornado.escape
import tornado.web
from settings import settings
from base import *
import requests
import re

class HomeHandler(BaseHandler):
    """
    """
    def get(self, video):
        if video == '':
            self.render_template("home.html")
        else:
            title = self.get_video_title(video)

            self.render_template("video.html",
                args={
                    'video': video,
                    'title': title,
            })

    def get_video_title(self, video):
        resource_data = requests.get('http://gdata.youtube.com/feeds/api/videos/' + video) 

        match = re.search(
            "<media:title.*?>(?P<title>.*)<\/media:title>", 
            resource_data.text)

        logging.info("match: " + str(match.group('title')))
        title = match.group('title') 

        return title
        



import tornado.auth
import tornado.escape
import tornado.web
from settings import settings
from base import *
import requests

class HomeHandler(BaseHandler):
    """
    """
    def get(self, video):
        self.render_template("home.html",
            args={
                'video': video
        })


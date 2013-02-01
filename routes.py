import os
from handlers.home import *
import importlib
import tornado.web

path = lambda root,*a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SANTA_ROOT = os.environ['SANTA_ROOT']
SRC_ROOT = path(ROOT, SANTA_ROOT)


"""DOCUMENTATION TODO"""
url_patterns = [
    (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "%s/static" % SRC_ROOT }),
    (r"/(.*)",                          HomeHandler),
]




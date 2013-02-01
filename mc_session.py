
import pylibmc 
from settings import settings

#memcache
mc = pylibmc.Client(
    servers=[settings['memcache_servers']],
    username=settings['memcache_username'],
    password=settings['memcache_password'],
    binary=True
)
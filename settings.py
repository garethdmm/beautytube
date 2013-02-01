import logging
import tornado
import tornado.template
import os
from os.path import dirname, abspath
from tornado.options import define, options
import environment



# Make filepaths relative to settings.
path = lambda root,*a: os.path.join(root, *a)
ROOT = dirname(dirname(abspath(__file__)))




environment_variables = os.environ

define("port", default=environment_variables['PORT'], help="run on the given port", type=int)
define("config", default=None, help="tornado config file")
define("debug", default=False, help="debug mode")
define("env", default=os.environ['SANTA_ENV'], help='Environment variable')
define('output_file', default='profile.out')
tornado.options.parse_command_line()

SANTA_ROOT = environment_variables['SANTA_ROOT']
MEDIA_ROOT = path(ROOT, SANTA_ROOT)
TEMPLATE_ROOT = path(ROOT, SANTA_ROOT)

# Deployment Configuration
class DeploymentType:
    PRODUCTION = "PRODUCTION"
    LOCAL_GARETH = "LOCALGARETH"
    LOCAL = "LOCAL"
    STAGING = "STAGING"
    dict = {
        PRODUCTION: 1,
        LOCAL: 2,
        STAGING: 3
    }

if options.env:
    DEPLOYMENT = options.env
else:
    DEPLOYMENT = DeploymentType.LOCAL

"""DOCUMENTATION TODO"""
settings = {}
settings['deployment']              = DEPLOYMENT
settings['debug']                   = DEPLOYMENT != DeploymentType.PRODUCTION or options.debug 
settings['xsrf_cookies']            = True
settings['template_loader']         = tornado.template.Loader(TEMPLATE_ROOT)
settings['login_url']               = '/facebook'
settings['database_cred']           = environment_variables['SANTA_DB_CRED']
settings['facebook_api_key']        = environment_variables['SANTA_FACEBOOK_API_KEY']
settings['facebook_secret']         = environment_variables['SANTA_FACEBOOK_SECRET']
settings['facebook_access_key']     = environment_variables['SANTA_FACEBOOK_ACCESS_KEY']
settings['domain']                  = environment_variables['SANTA_DOMAIN']
settings['cookie_secret']           = environment_variables['SANTA_COOKIE_SECRET']
settings['aws_key']                 = environment_variables['AWS_KEY']
settings['aws_secret_key']          = environment_variables['AWS_SECRET_KEY']
settings['memcache_servers']        = environment_variables['MEMCACHIER_SERVERS']
settings['memcache_username']       = environment_variables['MEMCACHIER_USERNAME']
settings['memcache_password']       = environment_variables['MEMCACHIER_PASSWORD']
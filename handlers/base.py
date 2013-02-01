# -*- coding: utf-8 -*-
import json
import tornado.web
import uuid
from settings import settings
from libs.error import error_handler
from models.user import User
from session import Session

import logging
logger = logging.getLogger(__name__)



class BaseHandler(tornado.web.RequestHandler):
    """A class to collect common handler methods - all other handlers should
    subclass this one.
    """
    tornado.web.RequestHandler.write_error = error_handler
    
    def get_current_user(self):
        """ 
            Returns the models.User object representing the currently
            logged in user.  
            
            The get_current_user will only work if the the user is both
            logged in and has purchased the film
            
            There is also an override for admin accounts
        """
        user = self.get_secure_cookie('user')
        return self.session.query(User).filter_by(link=user).first()
        
    
    def show_error_message(self, message):
        self.set_secure_cookie('error_message', message)

    def show_message(self, message):
        self.set_secure_cookie('message', message)
    
    def login_user(self, user):
        self.set_secure_cookie('user', user.link)
    
    def logout_user(self, user):
        self.clear_cookie('user')
       
    def prepare(self):
        p3p = 'CP="Like Facebook, Santa does not have a P3P policy -Learn why: http://fb.me/p3p"'
        self.add_header('Accept-Charset', 'utf-8')
        self.set_header('P3P', p3p)
        self.session = Session()
    
    def on_finish(self):
        try:
            self.session.commit()            
        except Exception as e:
            self.session.rollback()
            import traceback
            logging.critical('Transaction needed to be rolled back because of: \n %s' % traceback.format_exc() )
        Session.remove()
    
    
    def respond_with_json(self, success, message, other_info={}):
        response_object = {'success':success, 'message':message}
        response_object.update(other_info)
        self.write(json.dumps(response_object))
        return
    
    def render_template(self, template, **kwargs):
        """
            An extension to the render() function.
            This adds things linke message, google analytics key, facebook appid,
            mixpanel token and the current_user's name to the page at render time.
            The args parameter allows you to add adhoc variables to a page as well.
            
            Remember that the args variable must be accessed like args['vari'] in the
            tempalte.  
        """
      
        current_user = self.get_current_user()
        current_user_name = ''
        current_user_unique_id = ''
        user_has_purchased = False
            
        
        # Grab the cookie messages
        cookie_message = self.get_secure_cookie('message')
        error_message = self.get_secure_cookie('error_message')
        self.set_secure_cookie("message", '')
        self.set_secure_cookie("error_message", '')
        
        kwargs.update({
            'user':current_user,
            'error_message':error_message,
            'message':cookie_message,
            'facebook_api_key': settings['facebook_api_key'],
            'domain':settings['domain']
        })
        
        template = 'templates/%s'%template
        return self.render( template, **kwargs)
        


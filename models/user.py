from base import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum

import simplejson as json
import uuid
import datetime
from sqlalchemy.ext.declarative import declarative_base


metadata = Base.metadata


class User(Base):
    """Describes a facebook account. Maps to a user account.  """
    __tablename__ = 'facebook_account'
    
    #PK
    user_id = Column(Integer, primary_key=True)
    
    
    #Properties
    link = Column(String(2018), nullable=False)
    first_name = Column(String(512), nullable=False)
    last_name = Column(String(512), nullable=False)
    name = Column(String(512), nullable=False)
    locale = Column(String(512), nullable=False)
    session_expires = Column(String(512), nullable=False)
    access_token = Column(String(512), nullable=False)
    picture = Column(String(512), nullable=False)
    facebook_identifier = Column(String(128), nullable=False)
    time_added = Column(DateTime, nullable=False)
    time_updated = Column(DateTime, nullable=False)
    unique_id = Column(String(512), nullable=False)
    details = Column(String(10000), nullable=True)
    
    
    def __init__(self, facebook_dict):    
        self.picture            = facebook_dict['picture'].get('data').get('url') if facebook_dict['picture'].get('data') else facebook_dict['picture']
        self.first_name         = facebook_dict['first_name']
        self.last_name          = facebook_dict['last_name']
        self.name               = facebook_dict['name']
        self.locale             = facebook_dict['locale']
        self.session_expires    = str(facebook_dict['session_expires'][0])
        self.access_token       = facebook_dict['access_token']
        self.link               = facebook_dict['link']
        self.facebook_identifier= facebook_dict['id']
        self.time_added         = datetime.datetime.now()
        self.time_updated       = datetime.datetime.now()
        self.unique_id          = uuid.uuid4().hex
        self.details            = ''
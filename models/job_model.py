from base import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum

import simplejson as json
import uuid
import datetime
from sqlalchemy.ext.declarative import declarative_base


class Job(Base):
    """Describes a facebook account. Maps to a user account.  """
    __tablename__ = 'job'
    
    #PK
    job_id = Column(Integer, primary_key=True)
    
    
    #Properties
    job_key = Column(String(500), nullable=False)
    status = Column(Integer, nullable=False)
    message = Column(String(100000), nullable=False)
    function = Column(String(5000), nullable=False)
    time_started = Column(DateTime, nullable=False)
    time_finished = Column(DateTime, nullable=True)
    details = Column(String(10000), nullable=True)
    
    
    def __init__(self, function_called):    
       self.job_key = uuid.uuid4().hex
       self.status = 0
       self.message = 'Incomplete'
       self.function = function_called.__name__
       self.time_started = datetime.datetime.now()
       
       
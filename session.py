import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from settings import settings

engine = sqlalchemy.create_engine( settings['database_cred'] + '?charset=utf8', 
    echo=False, 
    pool_size = 100, 
    pool_recycle=3600)
Session = scoped_session(sessionmaker(bind=engine))

def get_a_session():
    from session import engine
    from sqlalchemy.orm import scoped_session, sessionmaker
    session = scoped_session(sessionmaker(bind=engine))
    return session



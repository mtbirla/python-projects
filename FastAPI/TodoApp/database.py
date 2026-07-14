from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import urllib.parse

user = 'postgres'
password = urllib.parse.quote_plus('Pass@123')

SQLALCHEMY_DB_URL = f'postgresql://{user}:{password}@localhost/TodoApplicationDb'

engine = create_engine(SQLALCHEMY_DB_URL) # here check_same_thread is set to false so all conn will be working on their separate thread and no same thread will be used to serve multiple request
SessionLocal = sessionmaker(autoflush=False, autocommit = False, bind = engine)
Base = declarative_base()
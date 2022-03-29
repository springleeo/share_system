# -*- coding: utf-8 -*-
import pathlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

username = 'root'
pwd = '12345678'
host = 'localhost'
port = '3306'
db_name = 'share_system'

# SQLALCHEMY_DATABASE_URL = 'sqlite:///' + str(pathlib.Path(__file__).parent.absolute()) + '/../data.sqlite3'
# Engine = create_engine(SQLALCHEMY_DATABASE_URL, encoding='utf-8', echo=True, connect_args={'check_same_thread': False})

url = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(username, pwd, host, port, db_name)
Engine = create_engine(url)

LocalSession = sessionmaker(bind=Engine)

Base = declarative_base()

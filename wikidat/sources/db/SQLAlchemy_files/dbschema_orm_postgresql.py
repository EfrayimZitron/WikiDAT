"""
Basic DB schema to import data from Wikipedia dump files using the SQLAlchemy Object Relational Mapper and 
the PyMySQL MySQL database connector. (MySQLdb seems to be more popular, but lacks support for Python 3.x)


"""
from sqlalchemy import Column, create_engine, text
from sqlalchemy.types import VARBINARY, DateTime
from sqlalchemy.dialects.postgresql import  TEXT, BYTEA, BOOLEAN, SMALLINT
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER
from sqlalchemy.ext.declarative import declarative_base
import psycopg2
import sys

Base = declarative_base()

dbengine = 'InnoDB'  # sys.argv[1]
params = {'mysql_engine': dbengine}


class Page(Base):
    __tablename__ = 'page'
    __table_args__ = params
    page_id = Column(INTEGER, nullable=False, primary_key=True)
    page_namespace = Column(SMALLINT, nullable=False)
    page_title = Column(VARCHAR(length=255, binary=True), nullable=False)
    page_restrictions = Column(BYTEA(256), nullable=False, server_default='')

    def __init__(self, page_id=None, page_namespace=None, page_title=None, page_restrictions=None):
        self.page_id = page_id
        self.page_namespace = page_namespace
        self.page_title = page_title
        self.page_restrictions = page_restrictions


class Revision(Base):
    __tablename__ = 'revision'
    __table_args__ = params
    rev_id = Column(INTEGER, nullable=False, primary_key=True)
    rev_page = Column(INTEGER, nullable=False)
    rev_user = Column(INTEGER, nullable=False, default=0)
    rev_timestamp = Column(DateTime, nullable=False)
    rev_len = Column(INTEGER, nullable=False)
    rev_parent_id = Column(INTEGER, nullable=True, server_default = text('NULL'))
    rev_is_redirect = Column(BOOLEAN, nullable=False, server_default='0')
    rev_minor_edit = Column(BOOLEAN, nullable=False, server_default='0')
    rev_fa = Column(BOOLEAN, nullable=False, server_default='0')
    rev_flist = Column(BOOLEAN, nullable=False, server_default='0')
    rev_ga = Column(BOOLEAN, nullable=False, server_default='0')
    rev_comment = Column(TEXT, nullable=False)

    def __init__(self, rev_id=None, rev_page=None, rev_user=None, rev_timestamp=None, rev_len=None,
                 rev_parent_id=None, rev_is_redirect=None, rev_minor_edit=None, rev_fa=None, rev_flist=None,
                 rev_ga=None, rev_comment=None):
        self.rev_id = rev_id
        self.rev_page = rev_page
        self.rev_user = rev_user
        self.rev_timestamp = rev_timestamp
        self.rev_len = rev_len
        self.rev_parent_id = rev_parent_id
        self.rev_is_redirect = rev_is_redirect
        self.rev_minor_edit = rev_minor_edit
        self.rev_fa = rev_fa
        self.rev_flist = rev_flist
        self.rev_ga = rev_ga
        self.rev_comment = rev_comment


class RevisionHash(Base):
    __tablename__ = 'revision_hash'
    __table_args__ = params
    rev_id = Column(INTEGER, nullable=False, primary_key=True)
    rev_page = Column(INTEGER, nullable=False)
    rev_user = Column(INTEGER, nullable=False, server_default = text('0'))
    rev_hash = Column(BYTEA(256), nullable=False)

    def __init__(self, rev_id=None, rev_page=None, rev_user=None, rev_hash=None):
        self.rev_id = rev_id
        self.rev_page = rev_page
        self.rev_user = rev_user
        self.rev_hash = rev_hash


class Namespaces(Base):
    __tablename__ = 'namespaces'
    __table_args__ = params
    code = Column(SMALLINT, nullable=False, primary_key=True)
    name = Column(VARCHAR(50), nullable=False)

    def __init__(self, code=None, name=None):
        self.code = code
        self.name = name


class People(Base):
    __tablename__ = 'people'
    __table_args__ = params
    rev_user = Column(INTEGER, nullable=False, server_default= text('0'), primary_key=True)
    rev_user_text = Column(VARCHAR(length=255, binary=True), nullable=True,  server_default='')

    def __init__(self, rev_user=None, rev_user_text=None):
        self.rev_user = rev_user
        self.rev_user_text = rev_user_text


class Logging(Base):
    __tablename__ = 'logging'
    __table_args__ = params
    log_id = Column(INTEGER, nullable=False, primary_key=True)
    log_type = Column(VARCHAR(length=15, binary=True), nullable=False)
    log_action = Column(VARCHAR(length=15, binary=True), nullable=False)
    log_timestamp = Column(DateTime, nullable=False)
    log_user = Column(INTEGER, nullable=False)
    log_username = Column(VARCHAR(length=255, binary=True), nullable=False, server_default='')
    log_namespace = Column(INTEGER(display_width=5), nullable=False, server_default = text('0'))
    log_title = Column(VARCHAR(length=255, binary=True), nullable=False, server_default='')
    log_comment = Column(VARCHAR(length=255, binary=True), nullable=False,server_default='')
    log_params = Column(VARCHAR(length=255, binary=True), nullable=False, server_default='')
    log_new_flag = Column(INTEGER, nullable=False, server_default=text('0'))
    log_old_flag = Column(INTEGER, nullable=False)

    def __init__(self, log_id=None, log_type=None, log_action=None, log_timestamp=None, log_user=None,
                 log_username=None, log_namespace=None, log_title=None, log_comment=None, log_params=None,
                 log_new_flag=None, log_old_flag=None):
        self.log_id = log_id
        self.log_type = log_type
        self.log_action = log_action
        self.log_timestamp = log_timestamp
        self.log_user = log_user
        self.log_username = log_username
        self.log_namespace = log_namespace
        self.log_title = log_title
        self.log_comment = log_comment
        self.log_params = log_params
        self.log_new_flag = log_new_flag
        self.log_old_flag = log_old_flag

		
class Block(Base):
    __tablename__ = 'block'
    __table_args__ = params
    block_id = Column(INTEGER, nullable=False, primary_key=True)
    block_action = Column(VARCHAR(length = 15, binary = True), nullable=False)
    block_user = Column(INTEGER, nullable=False)
    block_timestamp = Column(DateTime, nullable=False)
    block_target = Column(INTEGER, nullable=False)
    block_ip = Column(INTEGER(display_width= 10), nullable= False)
    block_duration = Column(INTEGER, nullable=False)

    def __init__(self, block_id=None, block_action = None, block_user=None, block_timestamp =None, block_target=None,
                 block_ip=None, block_duration=None):
        self.block_id = block_id
        self.block_action = block_action
        self.block_user = block_user
        self.block_timestamp = block_timestamp
        self.block_target = block_target
        self.block_ip = block_ip
        self.block_duration = block_duration
   
class NewUser(Base):
    __tablename__ = 'newuser'
    __table_args__ = params
    user_id = Column(INTEGER, nullable=False, primary_key=True)
    username = Column(VARCHAR(length = 255), nullable=False)
    user_timestamp = Column(DateTime, nullable=False)
    user_action = Column(VARCHAR(15), nullable=False)

    def __init__(self, user_id=None, username = None, user_timestamp=None,user_action=None):
        self.user_id = user_id
        self.username = username
        self.user_timestamp = user_timestamp
        self.user_action = user_action

		
class Right(Base):
    __tablename__ = 'right'
    __table_args__ = params
    right_id = Column(INTEGER, nullable=False, primary_key=True)
    right_username = Column(VARCHAR(length = 255), nullable=False)
    right_timestamp = Column(DateTime, nullable=False)
    right_old = Column(VARCHAR(length = 255), nullable=False)
    right_new = Column(VARCHAR(length = 255), nullable=False)

    def __init__(self, right_id=None, right_username = None, right_timestamp=None, right_old=None, right_new = None):
        self.right_id = right_id
        self.right_username = right_username
        self.right_timestamp = right_timestamp
        self.right_old = right_old
        self.right_new = right_new			
		

engine = create_engine('postgresql+psycopg2://postgres:root@localhost/wikidb')
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
	



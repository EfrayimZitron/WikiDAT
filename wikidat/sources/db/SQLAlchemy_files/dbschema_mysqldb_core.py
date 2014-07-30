"""
Basic DB schema to import data from Wikipedia dump files using the SQLAlchemy Object Relational Mapper and 
the PyMySQL MySQL database connector. (MySQLdb seems to be more popular, but lacks support for Python 3.x)


"""

from sqlalchemy import Table, Column, MetaData
from sqlalchemy.types import SMALLINT, VARBINARY
from sqlalchemy.dialects.mysql import INTEGER, DATETIME, TEXT, TINYINT, TINYBLOB, VARCHAR
from sqlalchemy import create_engine
import MySQLdb
import sys

metadata = MetaData()

dbengine = 'MyISAM'  # sys.argv[1]

page = Table('page', metadata,
    Column('page_id', INTEGER(unsigned=True), nullable=False),
    Column('page_namespace', SMALLINT, nullable = False),
    Column('page_title', VARCHAR(length=255, binary=True), nullable=False),
    Column('page_restrictions', TINYBLOB, nullable=False),
    mysql_engine= dbengine)


revision = Table('revision', metadata,
    Column('rev_id', INTEGER(unsigned=True), nullable=False),
    Column('rev_page', INTEGER(unsigned=True), nullable=False),
    Column('rev_user', INTEGER(unsigned=True), nullable=False, default=0),
    Column('rev_timestamp', DATETIME, nullable=False),
    Column('rev_len', INTEGER(unsigned=True), nullable=False),
    Column('rev_parent_id', INTEGER(unsigned=True), nullable=True, default = 'NULL'),
    Column('rev_is_redirect', TINYINT(display_width=1, unsigned=True), nullable=False, default=0),
    Column('rev_minor_edit', TINYINT(display_width=1, unsigned=True), nullable=False, default=0),
    Column('rev_fa', TINYINT(display_width=1, unsigned=True), nullable=False, default=0),
    Column('rev_flist', TINYINT(display_width=1, unsigned=True), nullable=False, default=0),
    Column('rev_ga', TINYINT(display_width=1, unsigned=True), nullable=False, default=0),
    Column('rev_comment', TEXT, nullable=False),
    mysql_engine= dbengine)


revision_hash = Table('revision_hash', metadata,
    Column('rev_id', INTEGER(unsigned=True), nullable=False),
    Column('rev_page', INTEGER(unsigned=True), nullable=False),
    Column('rev_user', INTEGER(unsigned=True), nullable=False, default=0),
    Column('rev_hash', VARBINARY(256), nullable=False),
    mysql_engine= dbengine)


namespaces = Table('namespaces', metadata,
    Column('code', SMALLINT, nullable=False),
    Column('name', VARCHAR(50), nullable=False),
    mysql_engine= dbengine)

	
people = Table('people', metadata,
    Column('rev_user', INTEGER(unsigned=True), nullable=False, default=0),
    Column('rev_user_text', VARCHAR(length=255, binary=True), nullable=True, default=''),
    mysql_engine= dbengine)


logging = Table('logging', metadata,
    Column('log_id', INTEGER(unsigned=True), nullable=False),
    Column('log_type', VARCHAR(length=15, binary=True), nullable=False),
    Column('log_action', VARCHAR(length=15, binary=True), nullable=False),
    Column('log_timestamp', DATETIME, nullable=False),
    Column('log_user', INTEGER(unsigned=True), nullable=False),
    Column('log_username', VARCHAR(length=255, binary=True), nullable=False, default=''),
    Column('log_namespace', INTEGER(display_width=5), nullable=False, default=0),
    Column('log_title', VARCHAR(length=255, binary=True), nullable=False, default=''),
    Column('log_comment', VARCHAR(length=255, binary=True), nullable=False, default=''),
    Column('log_params', VARCHAR(length=255, binary=True), nullable=False, default=''),
    Column('log_new_flag', INTEGER(unsigned=True), nullable=False, default=0),
    Column('log_old_flag', INTEGER(unsigned=True), nullable=False),
    mysql_engine= dbengine)

block = Table('block', metadata,
    Column('block_id', INTEGER(unsigned=True), nullable=False),
    Column('block_action', VARCHAR(length = 15, binary = True), nullable=False),
    Column('block_user', INTEGER(unsigned=True), nullable=False),
    Column('block_timestamp', DATETIME, nullable=False),
    Column('block_target', INTEGER, nullable=False),
    Column('block_ip', INTEGER(display_width= 10, unsigned=True), nullable= False),
    Column('block_duration', INTEGER(unsigned=True), nullable=False),
    mysql_engine= dbengine)

	
new_user = Table('new_user', metadata,
    Column('user_id',INTEGER(unsigned=True), nullable=False),
    Column('username', VARCHAR(length = 255), nullable=False),
    Column('user_timestamp', DATETIME, nullable=False),
    Column('user_action', VARCHAR(15), nullable=False),
    mysql_engine= dbengine)

	
right = Table('right', metadata,
    Column('right_id', INTEGER(unsigned=True), nullable=False),
    Column('right_username', VARCHAR(length = 255), nullable=False),
    Column('right_timestamp', DATETIME, nullable=False),
    Column('right_old', VARCHAR(length = 255), nullable=False),
    Column('right_new', VARCHAR(length = 255), nullable=False),
    mysql_engine= dbengine)
	
	
engine = create_engine('mysql+mysqldb://root:@localhost/')
engine.execute("DROP DATABASE IF EXISTS wikidb")
engine.execute("CREATE DATABASE IF NOT EXISTS wikidb CHARACTER SET utf8 COLLATE utf8_general_ci")  # create db
engine.execute("USE wikidb")
metadata.create_all(engine)
    



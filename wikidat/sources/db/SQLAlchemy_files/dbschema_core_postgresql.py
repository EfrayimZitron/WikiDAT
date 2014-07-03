"""
Basic DB schema to import data from Wikipedia dump files using the SQLAlchemy Object Relational Mapper and 
the psycogpg database connector to a Postgres database. 

Note: Script does not CREATE database, just the tables. There is some transactional violation or error when attempting to 
do both consecutively 

- Can't establish varhcars as binary types
- Can't seem to set rev_parent_id default to NULL
- Can't set width of integer for log_namespace
- Can't set page_restrictions or rev_hash to a binary BYTEA type; get "TypeError can't escape str to binary"
  This seems to be an issue exclusive to Python 3 as it handles string and bytes data differently than Py 2
"""

from sqlalchemy import Table, Column, MetaData, text
from sqlalchemy.types import VARBINARY, DateTime
from sqlalchemy.dialects.postgresql import  TEXT, BYTEA, BOOLEAN, SMALLINT
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER
from sqlalchemy import create_engine
import psycopg2
import sys

#Create metadata object which will hold table info
metadata = MetaData()

page = Table('page', metadata,
    Column('page_id', INTEGER, nullable=False),
    Column('page_namespace', SMALLINT, nullable = False),
    Column('page_title', VARCHAR(length=255, binary=True), nullable=False),
    Column('page_restrictions', BYTEA(256), nullable=False, server_default=''))

revision = Table('revision', metadata,
    Column('rev_id', INTEGER, nullable=False),
    Column('rev_page', INTEGER, nullable=False),
    Column('rev_user', INTEGER, nullable=False, server_default= text('0')),
    Column('rev_timestamp', DateTime, nullable=False),
    Column('rev_len', INTEGER, nullable=False),
    Column('rev_parent_id', INTEGER, nullable=True, server_default = text('NULL')),
    Column('rev_is_redirect', BOOLEAN, nullable=False, server_default='0'),
    Column('rev_minor_edit', BOOLEAN, nullable=False, server_default='0'),
    Column('rev_fa', BOOLEAN, nullable=False, server_default='0'),
    Column('rev_flist', BOOLEAN, nullable=False, server_default='0'),
    Column('rev_ga', BOOLEAN, nullable=False, server_default='0'),
    Column('rev_comment', TEXT, nullable=False))

revision_hash = Table('revision_hash', metadata,
    Column('rev_id', INTEGER, nullable=False),
    Column('rev_page', INTEGER, nullable=False),
    Column('rev_user', INTEGER, nullable=False, server_default = text('0')),
    Column('rev_hash', BYTEA(256), nullable=False))

namespaces = Table('namespaces', metadata,
    Column('code', SMALLINT, nullable=False),
    Column('name', VARCHAR(50), nullable=False))

people = Table('people', metadata,
    Column('rev_user', INTEGER, nullable=False, server_default= text('0')),
    Column('rev_user_text', VARCHAR(length=255, binary=True), nullable=True, server_default=''))

logging = Table('logging', metadata,
    Column('log_id', INTEGER, nullable=False),
    Column('log_type', VARCHAR(length=15, binary=True), nullable=False),
    Column('log_action', VARCHAR(length=15, binary=True), nullable=False),
    Column('log_timestamp', DateTime, nullable=False),
    Column('log_user', INTEGER, nullable=False),
    Column('log_username', VARCHAR(length=255, binary=True), nullable=False, server_default=''),
    Column('log_namespace', INTEGER(display_width=5), nullable=False, server_default = text('0')),
    Column('log_title', VARCHAR(length=255, binary=True), nullable=False, server_default=''),
    Column('log_comment', VARCHAR(length=255, binary=True), nullable=False, server_default=''),
    Column('log_params', VARCHAR(length=255, binary=True), nullable=False, server_default=''),
    Column('log_new_flag', INTEGER, nullable=False, server_default=text('0')),
    Column('log_old_flag', INTEGER, nullable=False))



engine = create_engine('postgresql+psycopg2://postgres:root@localhost/wikidb')
conn = engine.connect()
#conn = conn.execution_options(isolation_level="AUTOCOMMIT")
#conn.execute("DROP DATABASE IF EXISTS wikidb")
#conn.execute("CREATE DATABASE wikidb  ENCODING 'UTF8'")  # create db
#conn = conn.execution_options(isolation_level="READ COMMITTED")
metadata.drop_all(conn)
metadata.create_all(conn)
    




from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import MySQLdb
import csv
import sys
import dbschema_mysqldb_core
import timeit

engine = create_engine('mysql+mysqldb://root:@localhost/wikidb')
meta = MetaData()
meta.reflect(bind=engine)
page = meta.tables['page']
revision =  meta.tables['revision']
revision_hash = meta.tables['revision_hash']


def read_csv():
	"""
	Reads CSV files (for page, revision, and revision_hash) into data structure
	"""
	with open('page.csv') as page_file:
		fieldnames = ('page_id', 'page_namepsace', 'page_title', 'page_restrictions')
		reader = csv.DictReader(page_file, fieldnames = fieldnames, delimiter='\t')
		global page_dict
		page_dict = [row for row in reader]

	with open('revision.csv') as revision_file:
		fieldnames = ('rev_id', 'rev_page', 'rev_user', 'rev_timestamp', 'rev_len', 'rev_parent_id',
		'rev_is_redirect', 'rev_minor_edit', 'rev_fa', 'rev_flist', 'rev_ga', 'rev_comment')
		reader = csv.DictReader(revision_file, fieldnames = fieldnames, delimiter='\t')
		global revision_dict
		revision_dict = []
		for row in reader:
			if row['rev_parent_id'] == 'NULL':
				row['rev_parent_id'] = None 
			revision_dict.append(row)

	with open('revision_hash.csv') as revision_hash_file:
		fieldnames = ('rev_id', 'rev_page', 'rev_user', 'rev_hash')
		reader = csv.DictReader(revision_hash_file, fieldnames = fieldnames, delimiter='\t')
		global revision_hash_dict
		revision_hash_dict = [row for row in reader]


def load():
	"""
	Performs the actual insertions into the database
	"""
	engine.execute(page.insert(),page_dict)

	engine.execute(revision.insert(),revision_dict)

	engine.execute(revision_hash.insert(),revision_hash_dict) 
	

timer = timeit.Timer(stmt='load()', setup='from testload_mysqldb_core import load')	

def run_time_test():
	"""
	Deletes and recreates the database, and performs one run of inserts
	"""
	meta.drop_all(engine)
	meta.create_all(engine)   
	return(timer.timeit(number=1))

def bulk_insert():
	read_csv()
	total = []
	for x in range(1):
		total.append(run_time_test())
		print 'Run', x, 'took', total[x]

	print 'The fastest run was:', min(total), 'secs'    
	print 'Average running time:', sum(total)/len(total)

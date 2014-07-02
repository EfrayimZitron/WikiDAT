
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import statistics
import psycopg2
import csv
import sys
import dbschema_core_postgresql
import timeit


engine = create_engine('postgresql+psycopg2://postgres:root@localhost/wikidb')

with open('page.csv', newline = '' , encoding = 'utf-8') as page_file:
    fieldnames = ('page_id', 'page_namespace', 'page_title', 'page_restrictions')
    reader = csv.DictReader(page_file, fieldnames = fieldnames, delimiter='\t')
    page_dict = [row for row in reader]
    for row in page_dict:
        row['page_namespace'] = int(row.get('page_namespace'))
    


with open('revision.csv', newline = '' , encoding = 'utf-8') as revision_file:
    fieldnames = ('rev_id', 'rev_page', 'rev_user', 'rev_timestamp', 'rev_len', 'rev_parent_id',
                  'rev_is_redirect', 'rev_minor_edit', 'rev_fa', 'rev_flist', 'rev_ga', 'rev_comment')
    reader = csv.DictReader(revision_file, fieldnames = fieldnames, delimiter='\t')
    revision_dict = [row for row in reader]

with open('revision_hash.csv', newline = '' , encoding = 'utf-8') as revision_hash_file:
    fieldnames = ('rev_id', 'rev_page', 'rev_user', 'rev_hash')
    reader = csv.DictReader(revision_hash_file, fieldnames = fieldnames, delimiter='\t')
    revision_hash_dict = [row for row in reader]

def load():
    engine.execute(dbschema_core_postgresql.page.insert(),page_dict)
	
    engine.execute(dbschema_core_postgresql.revision.insert(),revision_dict)

    engine.execute(dbschema_core_postgresql.revision_hash.insert(),revision_hash_dict)  
    

timer = timeit.Timer(stmt='load()', setup='from __main__ import load')

total = []

def run_time_test():
    dbschema_core_postgresql.metadata.drop_all(engine)
    dbschema_core_postgresql.metadata.create_all(engine)    
    return(timer.timeit(number=1))

for x in range(int(sys.argv[1])):
    total.append(run_time_test())
    print ('Run', x, 'took', total[x], 'secs')
    
#print ('Average running time:', sum(total)/len(total))
print ('The fastest run was:', min(total), 'secs')
print ('Average running time:', statistics.mean(total), 'secs')
print ('Standard Deviation:', statistics.stdev(total), 'secs')




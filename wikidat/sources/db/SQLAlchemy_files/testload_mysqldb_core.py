
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import MySQLdb
import csv
import sys
import dbschema_mysqldb_core
import timeit

engine = create_engine('mysql+mysqldb://root:@localhost/wikidb')

with open('page.csv') as page_file:
    fieldnames = ('page_id', 'page_namepsace', 'page_title', 'page_restrictions')
    reader = csv.DictReader(page_file, fieldnames = fieldnames, delimiter='\t')
    page_dict = [row for row in reader]

with open('revision.csv') as revision_file:
    fieldnames = ('rev_id', 'rev_page', 'rev_user', 'rev_timestamp', 'rev_len', 'rev_parent_id',
                  'rev_is_redirect', 'rev_minor_edit', 'rev_fa', 'rev_flist', 'rev_ga', 'rev_comment')
    reader = csv.DictReader(revision_file, fieldnames = fieldnames, delimiter='\t')
    revision_dict = []
    for row in reader:
        if row['rev_parent_id'] == 'NULL':
            row['rev_parent_id'] = None 
        revision_dict.append(row)
    

with open('revision_hash.csv') as revision_hash_file:
    fieldnames = ('rev_id', 'rev_page', 'rev_user', 'rev_hash')
    reader = csv.DictReader(revision_hash_file, fieldnames = fieldnames, delimiter='\t')
    revision_hash_dict = [row for row in reader]


def load():
    engine.execute(dbschema_mysqldb_core.page.insert(),page_dict)

    engine.execute(dbschema_mysqldb_core.revision.insert(),revision_dict)

    engine.execute(dbschema_mysqldb_core.revision_hash.insert(),revision_hash_dict) 

# Timer calculates how much time it takes for the data to be loaded into the database.
# Had to specify that the timer should only run one execution of the code since multiple runs of inserting identical
# data would fail due to primary key violations
timer = timeit.Timer(stmt='load()', setup='from __main__ import load')

total = []

def run_time_test():
    dbschema_mysqldb_core.metadata.drop_all(engine)
    dbschema_mysqldb_core.metadata.create_all(engine)   
    return(timer.timeit(number=1))
    
for x in range(int(sys.argv[1])):
    total.append(run_time_test())
    print 'Run', x, 'took', total[x]

print 'The fastest run was:', min(total), 'secs'    
print 'Average running time:', sum(total)/len(total)

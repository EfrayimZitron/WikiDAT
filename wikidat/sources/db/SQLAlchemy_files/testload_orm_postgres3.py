"""
Script loads sample data into database, using  the MySQLsb connector and Python 2.x as opposed to the PyMySQL connector for 3.x
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2
import csv
import sys
import dbschema_orm_postgresql
import timeit
import statistics

 #loads data from csv file into a list (of lists)
with open('page.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter='\t')
    page_data = []
    for row in reader:
        row[3] =  row[3].encode('utf-8')
        page_data.append(row) 	

with open('revision.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter='\t')
    revision_data = []
    for row in reader:
        if row[5] == 'NULL':
            row[5] = None 
        revision_data.append(row)

with open('revision_hash.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter='\t')
    revision_hash_data = []
    for row in reader:
        row[3] =  row[3].encode('utf-8')
        revision_hash_data.append(row) 


#Inserts data into database
#For larger data sets, it would probably be safer to instruct periodical commits every 100K queries
#or so, so that the computer wont hang, but it depends on the computer
def load():
    for item in page_data:
        session.add(dbschema_orm_postgresql.Page(*item))
    session.commit()

    for item in revision_data:
        session.add(dbschema_orm_postgresql.Revision(*item))
    session.commit()

    for item in revision_hash_data:
        session.add(dbschema_orm_postgresql.RevisionHash(*item))
    session.commit()

# Had to specify that the timer should only run one execution of the code since multiple runs of inserting identical
# data would fail due to primary key violations
def run_time_test():
    dbschema_orm_postgresql.Base.metadata.drop_all(engine)
    dbschema_orm_postgresql.Base.metadata.create_all(engine)	
    return(timer.timeit(number=1))
	
# Had to append '/?charset=utf8' to the create_engine string since there were encoding errors (UnicodeEncodeErrors)
# when I ran the script without it. 
engine = create_engine('postgresql+psycopg2://postgres:root@localhost/wikidb')
Session = sessionmaker(bind=engine)
session = Session()

# Timer calculates how much time it takes for the data to be loaded into the database.
timer = timeit.Timer(stmt='load()', setup='from __main__ import load')

total = []
	
for x in range(int(sys.argv[1])):
	total.append(run_time_test())
	print ('Run', x, 'took', total[x])

print ('The fastest run was:', min(total), 'secs')
print ('Average running time:', sum(total)/len(total), 'secs')
print ('Standard Deviation:', statistics.stdev(total), 'secs')
	


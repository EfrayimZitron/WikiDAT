"""
Inserts sample data into database using SQLAlchemy ORM and PyMySQL database connector -(python  syntax).
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pymysql
import csv
import sys
import dbschema_orm
import timeit

# loads data from csv file into a list (of lists)
with open('page.csv') as f:
    reader = csv.reader(f, delimiter='\t')
    page_data = list(list(row) for row in reader)

with open('revision.csv') as f:
    reader = csv.reader(f, delimiter='\t')
    revision_data = list(list(row) for row in reader)

with open('revision_hash.csv') as f:
    reader = csv.reader(f, delimiter='\t')
    revision_hash_data = list(list(row) for row in reader)


#Inserts data into database
#For larger data sets, it would probably be safer to instruct periodical commits every 100K queries
#or so, so that the computer wont hang, but it depends on the computer
def load():
    for item in page_data:
        session.add(dbschema_orm.Page(*item))
    session.commit()

    for item in revision_data:
        session.add(dbschema_orm.Revision(*item))
    session.commit()

    for item in revision_hash_data:
        session.add(dbschema_orm.RevisionHash(*item))
    session.commit()

# Had to specify that the timer should only run one execution of the code since multiple runs of inserting identical
# data would fail due to primary key violations
def run_time_test():
    dbschema_orm.Base.metadata.drop_all(engine)
    dbschema_orm.Base.metadata.create_all(engine)	
    return(timer.timeit(number=1))
	
# Had to append '/?charset=utf8' to the create_engine string since there were encoding errors (UnicodeEncodeErrors)
# when I ran the script without it. 
engine = create_engine('mysql+pymysql://root:@localhost/?charset=utf8')
engine.execute("USE wikidb")
Session = sessionmaker(bind=engine)
session = Session()

# Timer calculates how much time it takes for the data to be loaded into the database.
timer = timeit.Timer(stmt='load()', setup='from __main__ import load')

total = []
	
for x in range(int(sys.argv[1])):
	total.append(run_time_test())
	print 'Run', x, 'took', total[x]

print 'The fastest run was:', min(total), 'secs'
print 'Average running time:', sum(total)/len(total), 'secs'
	

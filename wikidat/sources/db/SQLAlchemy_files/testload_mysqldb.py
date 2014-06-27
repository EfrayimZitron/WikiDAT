
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import MySQLdb
import csv
import sys
import dbschema_mysqldb
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




# Had to append '/?charset=utf8' to the create_engine string since there were encoding errors (UnicodeEncodeErrors)
# when I ran the script without it. 
engine = create_engine('mysql+mysqldb://root:@localhost')
engine.execute("USE wikidb")
Session = sessionmaker(bind=engine)
session = Session()

#For larger data sets, it would probably be safer to instruct periodical commits every 100K queries
#or so, so that the computer wont hang, but it depends on the computer
def load():
    for item in page_data:
        session.add(dbschema_mysqldb.Page(*item))
    session.commit()

    for item in revision_data:
        session.add(dbschema_mysqldb.Revision(*item))
    session.commit()

    for item in revision_hash_data:
        session.add(dbschema_mysqldb.RevisionHash(*item))
    session.commit()


# Timer calculates how much time it takes for the data to be loaded into the database.
# Had to specify that the timer should only run one execution of the code since multiple runs of inserting identical
# data would fail due to primary key violations
timer = timeit.Timer(stmt='load()', setup='from __main__ import load')

total = []

def run_time_test():
    dbschema_mysqldb.Base.metadata.drop_all(engine)
    dbschema_mysqldb.Base.metadata.create_all(engine)	
    return(timer.timeit(number=1))

for x in range(int(sys.argv[1])):
	total.append(run_time_test())
	print 'Run', x, 'took', total[x]
	
print 'Average running time:', sum(total)/len(total)

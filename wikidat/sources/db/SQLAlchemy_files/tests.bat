ECHO Python 3.4 + PyMySQL + SQLAlchemy Core > results.txt
C:\Python34\python.exe C:\Users\Efi\Documents\GitHub\WikiDAT\wikidat\sources\db\SQLAlchemy_files\testload_core.py 100 >> results.txt
ECHO Python 3.4 + PyMySQL + SQLAlchemy ORM >> results.txt
C:\Python34\python.exe C:\Users\Efi\Documents\GitHub\WikiDAT\wikidat\sources\db\SQLAlchemy_files\testload_orm.py 100 >> results.txt
ECHO Python 2.7 + PyMySQL + SQLAlchemy Core >> results.txt
C:\Python27\python2.exe C:\Users\Efi\Documents\GitHub\WikiDAT\wikidat\sources\db\SQLAlchemy_files\testload_core2.py 100 >> results.txt
ECHO Python 2.7 + PyMySQL + SQLAlchemy ORM >> results.txt
C:\Python27\python2.exe C:\Users\Efi\Documents\GitHub\WikiDAT\wikidat\sources\db\SQLAlchemy_files\testload_orm2.py 100 >> results.txt
ECHO Python 2.7 + MySQLdb + SQLAlchemy Core >> results.txt
C:\Python27\python2.exe C:\Users\Efi\Documents\GitHub\WikiDAT\wikidat\sources\db\SQLAlchemy_files\testload_mysqldb_core.py 100 >> results.txt
ECHO Python 2.7 + MySQLdb + SQLAlchemy ORM >> results.txt
C:\Python27\python2.exe C:\Users\Efi\Documents\GitHub\WikiDAT\wikidat\sources\db\SQLAlchemy_files\testload_mysqldb_orm.py 100 >> results.txt
ECHO Python 2.7 + psycopg + SQLAlchemy Core >> results.txt
C:\Python27\python2.exe C:\Users\Efi\Documents\GitHub\WikiDAT\wikidat\sources\db\SQLAlchemy_files\testload_core_postgres2.py 100 >> results.txt
ECHO Python 3.4 + psycopg + SQLAlchemy Core >> results.txt
C:\Python34\python.exe C:\Users\Efi\Documents\GitHub\WikiDAT\wikidat\sources\db\SQLAlchemy_files\testload_core_postgres3.py 100 >> results.txt
ECHO Python 3.4 + psycopg + SQLAlchemy ORM >> results.txt
C:\Python34\python.exe C:\Users\Efi\Documents\GitHub\WikiDAT\wikidat\sources\db\SQLAlchemy_files\testload_orm_postgres3.py 100 >> results.txt
ECHO Python 2.7 + psycopg + SQLAlchemy ORM >> results.txt
C:\Python27\python2.exe C:\Users\Efi\Documents\GitHub\WikiDAT\wikidat\sources\db\SQLAlchemy_files\testload_orm_postgres2.py 100 >> results.txt
PAUSE
"""
Test inserting nulls in a database.
"""

import psycopg2 as dbapi
from dbapiext import execute_f


conn = dbapi.connect(host='localhost',
                     database='test',
                     user='blais',
                     password='pg')

curs = conn.cursor()
curs.execute("""

   CREATE TABLE test1 (
     id SERIAL,
     namea VARCHAR(120),
     nameb VARCHAR(120) DEFAULT NULL,

     PRIMARY KEY(id)
   );

  """)


curs.execute("""
  INSERT INTO test1 (namea, nameb) VALUES (%S, %S);
""", (None, None))

conn.commit()


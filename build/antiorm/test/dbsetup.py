#!/usr/bin/env python

"""
Connection parameters for tests.
"""

# antiorm imports
from antiorm import *



connect_params = dict(database='test',
                      host='localhost',
                      user='blais',
                      password='pg')



def prepare_testdb(conn):
    """
    Prepare a test database.
    """
    # First drop all existing tables to prepare the test database.
    curs = conn.cursor()
    curs.execute("""SELECT table_name FROM information_schema.tables
                      WHERE table_schema = 'public'""")
    for table_name in curs.fetchall():
        curs.execute("DROP TABLE %s" % table_name)

    curs.execute("""

      CREATE TABLE test1 (
        id serial primary key,
        firstname text,
        lastname text,
        religion text,
        creation date
      );

      CREATE TABLE test2 (
        id serial primary key,
        motto text
      )

      """)
    conn.commit()


# Declare testing table
class TestTable(MormTable):
    table = 'test1'
    converters = {
        'firstname': MormConvUnicode(),
        'lastname': MormConvUnicode(),
        'religion': MormConvString()
        }

# Declare testing table
class TestTable2(MormTable):
    table = 'test2'
    converters = {
        'motto': MormConvUnicode(),
        }



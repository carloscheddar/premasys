#!/usr/bin/env python
"""
Test forking a parent process that has a connection pool.
"""

from __future__ import with_statement

import sys, os, traceback, string, random, antipool
from time import sleep
from antipool import *
from os import fork
import psycopg2 as dbapi




def do_something():
    trace('do_something')
    with dbpool().connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
          INSERT INTO bullshit (no, name) VALUES (%d, '%s');
            """ % (random.randint(0, 100), ''.join(random.sample(string.letters, 10))))
    trace('/do_something')


def main():
    import optparse
    parser = optparse.OptionParser(__doc__.strip())
    opts, args = parser.parse_args()

    pool = ConnectionPool(dbapi,
                          dict(debug=sys.stderr),
                          host='localhost',
                          user='postgres',
                          database='test',
                          )
    antipool.initpool(pool)




    # Create some temporary table and insert shit into it.
    with dbpool().connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""

          DROP TABLE bullshit;

          CREATE TABLE bullshit (
             no int,
             name text
          );

        """)
        conn.commit()

    do_something()


    try:
        for _ in xrange(2):
            fork_party()
    except Exception, e:
        trace('pid %s' % os.getpid())
        traceback.print_exc()
        traceback.print_exc(file=open('/tmp/out.%s' % os.getpid(), 'w'))
        raise
        



def fork_party():

    # Fork the process.
    pid = fork()
    if pid != 0:
        trace('parent')
        do_something()
        sleep(random.random())
            
    else:
        trace('child')
        dbpool().forget_connections()
        do_something()
        sleep(random.random())


        
if __name__ == '__main__':
    main()

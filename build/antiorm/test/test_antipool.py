#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

"""
Tests for connection pool.
"""

# stdlib imports
import threading
from datetime import datetime, timedelta

# antiorm imports
from antipool import *



names = ('martin', 'cyriaque', 'pierre', 'mathieu', 'marie-claude', 'eric'
         'normand', 'christine', 'emric')

class ConnectionPoolPoser(ConnectionPool):
    """
    A fake pool of database connections, that does not pool at all but that
    behaves as if it did.  We use this for implementing performance comparisons
    in the tests.
    """
    def _get_connection_ro(self):
        return self._create_connection(True)

    def _get_connection(self):
        return self._create_connection(False)
        
    def _release_ro(self, conn):
        self._close(conn)
        
    def _release(self, conn):
        self._close(conn)


class Stats(object):
    """
    An object that has a lock on it that you can use for mut.ex.
    """
    def __init__(self):
        self._lock = threading.Lock()

        self.ops_ro = 0
        self.ops_rw = 0

    def inc_ops_ro(self):
        self._lock.acquire()
        self.ops_ro += 1
        self._lock.release()
        
    def inc_ops_rw(self):
        self._lock.acquire()
        self.ops_rw += 1
        self._lock.release()

class TestThreads(threading.Thread):

    def __init__(self, opts, stats):
        threading.Thread.__init__(self)

        self.opts = opts
        self.stats = stats
        self._stop = False

    def stop(self):
        self._stop = True

    def run(self):
        timeout = (datetime.now() + timedelta(seconds=self.opts.timeout))

        while not self._stop and datetime.now() < timeout:
            time.sleep(random.uniform(0, self.opts.time_wait))

            conn = None
            try:
                if random.random() < self.opts.prob_ro:
                    # Read-only operation.
                    conn = dbpool.connection_ro()

                    curs = conn.cursor()
                    curs.execute("""
                      SELECT name FROM things LIMIT %s;
                      """ % random.randint(0, 5))
                    dbpool._log('SELECT %s\n' % ','.join(
                        map(lambda x: x[0], curs.fetchall())))
                    self.stats.inc_ops_ro()

                else:
                    conn = dbpool.connection()

                    curs = conn.cursor()
                    things = (random.choice(names), self.getName())
                    dbpool._log('INSERT %s\n' % (things,))
                    curs.execute("""
                      INSERT INTO things (name, thread) VALUEs (%s, %s);
                      """, things)
                    conn.commit()
                    self.stats.inc_ops_rw()

            finally:
                time.sleep(self.opts.time_hold)
                if random.random() < self.opts.prob_forget:
                    if conn is not None:
                        conn.release()


def test():
    import optparse
    parser = optparse.OptionParser(__doc__.strip())

    parser.add_option('--debug', action='store_true',
                      help="Enable debugging output.")

    parser.add_option('--threads', '--nb-threads', action='store', type='int',
                      default=10,
                      help="Number of threads to create.")

    parser.add_option('--prob-ro', action='store', type='float',
                      default=0.8,
                      help="Specify the read-only to read-and-write ratio "
                      "as a PDF.")

    parser.add_option('--prob-forget', action='store', type='float',
                      default=0.1,
                      help="Probability to forget to release the connection.")

    parser.add_option('--timeout', action='store', type='float',
                      default=10,
                      help="Total time for the experiment")

    parser.add_option('-w', '--time-wait', '--wait',
                      action='store', type='float', default=2.0, metavar='SECS',
                      help="Maximum time to wait between each operations.")

    parser.add_option('-H', '--time-hold', '--hold',
                      action='store', type='float', default=0.1, metavar='SECS',
                      help="Time to hold a connection for an operation.")
    
    parser.add_option('-s', '--time-stats', action='store', type='float',
                      default=0.2, metavar='SECS',
                      help="Time to pool the connection pool for statistics. "
                      "This will determine the resolution of the graph "
                      "generated.")

    parser.add_option('--minconn', action='store', type='int',
                      default=3,
                      help="Minimum number of connections to keep around when "
                      "scaling down the pool.")

    parser.add_option('--maxconn', action='store', type='int',
                      default=8,
                      help="Maximum number of connections to create in all.")

    parser.add_option('--minkeepsecs', action='store', type='float',
                      default=5,
                      help="Default seconds to keep a connection for when "
                      "scaling down the pool.")

    parser.add_option('--disable-ro', action='store_true',
                      help="Disable the read-only optimization.")

    parser.add_option('--poser', action='store_true',
                      help="Do not really use connection pooling but rather "
                      "connect and close everytime.")

    parser.add_option('--graph', '--generate-graph', action='store',
                      default=None, metavar='FILE', 
                      help="Generate a graph in the given filename.")

    opts, args = parser.parse_args()

    if opts.graph:
        opts.graph = open(opts.graph, 'w')
        
    poolcls = ConnectionPool
    if opts.poser:
        poolcls = ConnectionPoolPoser
    
    import psycopg2
    
    options=dict(minconn=opts.minconn,
                 maxconn=opts.maxconn,
                 minkeepsecs=opts.minkeepsecs,
                 disable_ro=opts.disable_ro,
                 debug=opts.debug and sys.stderr or None)

    global dbpool
    dbpool = poolcls(psycopg2,
                     options=options.copy(),
                     database='test',
                     user='blais')

    # Create some tables.
    conn = dbpool.connection()
    try:
        curs = conn.cursor()
        try:
            curs.execute(test_drop)
        except psycopg2.Error:
            conn.rollback()
        curs.execute(test_schema)
        conn.commit()
    finally:
        conn.release()

    # Create a global object to accumulate statistics.
    stats = Stats()

    up_and_down = 0
    if up_and_down:
        conns = []
        for i in xrange(10):
            conns.append(dbpool.connection())

        for conn in conns:
            conn.release()

        sys.exit(0)

    # Create threads that operate concurrently on that table.
    threads = []
    for i in xrange(opts.threads):
        t = TestThreads(opts, stats)
        threads.append(t)

    # Start timer.
    time_a = time.time()

    # Start threads.
    for t in threads:
        t.start()
    
    try:
        while time.time() - time_a < opts.timeout:
            time.sleep(opts.time_stats)
            if opts.graph:
                opts.graph.write('%d %d\n' % dbpool.getstats())
    except KeyboardInterrupt:
        print 'Interrupted.'
        for t in threads:
            t.stop()

    for t in threads:
        t.join()

    time_b = time.time()

    dbpool.finalize()

    interval = time_b - time_a
    print 'Options:'
    for key, value in options.iteritems():
        print '  %s: %s' % (key, value)
    print ('Statistics:  %f RO ops/sec   %f RW ops/sec' % 
           (float(stats.ops_ro)/interval, float(stats.ops_rw)/interval))


test_drop = '''

  DROP TABLE things;

'''

test_schema = '''

  CREATE TABLE things (

      id SERIAL PRIMARY KEY,
      name TEXT,
      thread TEXT

  );

'''

if __name__ == '__main__':
    import sys, random, time
    log_write = sys.stdout.write
    test()




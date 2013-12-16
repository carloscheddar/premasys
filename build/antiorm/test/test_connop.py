#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# pylint: disable-msg=W0302

"""
Tests for Anti-ORM.
"""

# stdlib imports
import unittest

# antiorm imports
from antiorm import *

# test imports
from dbsetup import *



import antipool
from antipool import ConnOp

class TestPool(unittest.TestCase):
    """
    Test using the connection pool.
    """
    conn = None

    def setUp(self):
        # Create a connection pool and register it.
        thepool = antipool.ConnectionPool(dbapi, **connect_params)
        antipool.initpool(thepool)

        conn = thepool.connection()
        try:
            prepare_testdb(conn)
        finally:
            conn.release()

    def test_simple(self):
        """
        Simple test.
        """
        
        print '\nBEFORE'
        for o in ConnOp(TestTable).select_all():
            print o.firstname, o.lastname

        ConnOp(TestTable).insert(firstname=u'Adriana',
                                 lastname=u'Sousa',
                                 religion='candomblé')

        print '\nAFTER'
        for o in ConnOp(TestTable).select_all():
            print o.firstname, o.lastname


def suite():
    thesuite = unittest.TestSuite()
    thesuite.addTest(TestPool("test_simple"))
    return thesuite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')



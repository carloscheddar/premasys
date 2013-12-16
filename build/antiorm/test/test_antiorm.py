# -*- coding: iso-8859-1 -*-
# pylint: disable-msg=W0302

"""
Tests for Anti-ORM.
"""

# stdlib imports
from datetime import datetime
import unittest

# antiorm imports
from antiorm import *

# test imports
from dbsetup import *



class TestMorm(unittest.TestCase):
    """
    Simple automated tests.
    This also acts as examples and documentation.
    """
    conn = None

    def setUp(self):
        # Connect to the database.
        if TestMorm.conn is None:
            TestMorm.conn = dbapi.connect(**connect_params)

            prepare_testdb(TestMorm.conn)

        self.conn = TestMorm.conn

    def test_insert(self):
        """
        Test methods for encoding and for insertion.
        """
        conn = self.conn

        #
        # Use an explicit encoder object to fill SQL statements.
        #
        enc = TestTable.encoder(firstname=u'Marité',
                                lastname=u'Lubrí',
                                religion='santería')
        curs = conn.cursor()
        curs.execute("INSERT INTO %s (%s) VALUES (%s)" %
                     (enc.table(), enc.cols(), enc.plhold()),
                     enc.values())
        conn.commit()

        #
        # INSERT on the encoder object.
        #
        enc = TestTable.encoder(firstname=u'Yanní',
                                lastname=u'Calumà',
                                religion='santería')
        enc.insert(conn)
        conn.commit()

        #======================================================================\

        #
        # INSERT on the table (the high-level, normal cases).
        #
        TestTable.insert(conn,
                         firstname=u'Adriana',
                         lastname=u'Sousa',
                         religion='candomblé')
        conn.commit()

        #======================================================================/


    def test_select(self):
        """
        Test methods for selecting.
        """
        conn = self.conn

        #
        # Decode explicitly, using the decoder object.
        #

        # Without restricting column names
        curs = conn.cursor()
        curs.execute("SELECT * FROM %s WHERE religion = %%s" %
                     (TestTable.tname()), (u'santería',))
        dec = TestTable.decoder(curs)
        for row in curs:
            self.assert_(dec.decode(row).firstname)
            self.assert_(dec.decode(row).lastname)
            self.assert_(dec.decode(row).religion)

        # With restricting column names.
        dec = TestTable.decoder( ('firstname',) )
        curs.execute("SELECT %s FROM %s WHERE religion = %%s" %
                     (dec.cols(), dec.table()), (u'santería',))
        for row in curs:
            self.assert_(dec.decode(row).firstname)

        # With a custom class.
        class MyClass:
            "Dummy class to be created to receive values"
        dec = TestTable.decoder(curs)
        curs.execute("SELECT %s FROM %s WHERE religion = %%s" %
                     (dec.cols(), dec.table()), (u'santería',))
        for row in curs:
            self.assert_(isinstance(dec.decode(row, objcls=MyClass), MyClass))

        # With a custom object.
        myinst = MyClass()
        dec = TestTable.decoder(curs)
        curs.execute("SELECT %s FROM %s WHERE religion = %%s" %
                     (dec.cols(), dec.table()), (u'santería',))
        for row in curs:
            self.assert_(isinstance(dec.decode(row, obj=myinst), MyClass))

        # Using the iterator protocol.
        dec = TestTable.decoder(curs)
        curs.execute("SELECT %s FROM %s WHERE religion = %%s" %
                     (dec.cols(), dec.table()), (u'santería',))
        for obj in dec.iter(curs):
            self.assert_(isinstance(obj, MormObject))

        # Test that it also works with empty results.
        for obj in dec.iter(curs):
            self.assert_(False)

        #
        # SELECT on the decoder object.
        #

        # With condition
        cursor = MormDecoder.do_select(conn, (TestTable,),
                                       cond='WHERE religion = %s',
                                       args=(u'santería',))
        it = MormDecoder(TestTable, cursor).iter(cursor)
        self.assert_(len(it))
        for obj in it:
            self.assert_(obj.firstname)
            self.assert_(obj.lastname)
            self.assert_(obj.religion)

        # Without condition
        cursor = MormDecoder.do_select(conn, (TestTable,))
        dec = MormDecoder(TestTable, cursor)
        for obj in dec.iter(cursor):
            self.assert_(obj.firstname and obj.lastname and obj.religion)

        # Using cursor on the decoder itself
        dec = MormDecoder(TestTable, cursor)
        for obj in dec.iter(cursor):
            self.assert_(obj.firstname and obj.lastname and obj.religion)

        #======================================================================\

        #
        # SELECT on the table (the high-level, normal cases).
        #

        # Without condition.
        for obj in TestTable.select(conn):
            self.assert_(obj.firstname and obj.lastname and obj.religion)

        # With condition.
        for obj in TestTable.select(conn, 'WHERE id = %s', (2,)):
            self.assert_(obj.firstname and obj.lastname and obj.religion)

        # With restricted columns.
        it = TestTable.select(conn, cols=('firstname',))
        self.assert_(len(it) == 3)
        for obj in it:
            self.assert_(obj.firstname)
            self.assertRaises(AttributeError, getattr, obj, 'lastname')

        # With dotted names.
        for obj in TestTable.select(conn, cols=('test1.firstname',)):
            self.assert_(obj.firstname)
            self.assertRaises(AttributeError, getattr, obj, 'lastname')

        # Select all.
        it = TestTable.select_all(conn)
        assert it
        for obj in it:
            self.assert_(obj.firstname)

        # Select one
        obj = TestTable.select_one(conn, 'WHERE id = %s', (42,))
        self.assert_(obj is None)
        self.assertRaises(MormError, TestTable.select_one, conn)
        obj = TestTable.select_one(conn, 'WHERE id = %s', (2,))
        self.assert_(obj is not None)

        # Empty select.
        it = TestTable.select(conn, 'WHERE id = %s', (2843732,))
        self.assert_(len(it) == 0)
        self.assert_(not it)
        self.assertRaises(StopIteration, it.next)

        #======================================================================/

    def test_count(self):
        """
        Test methods for counting rows/matches.
        """
        conn = self.conn

        self.assertEquals(TestTable.count(conn), 3)


    def test_get(self):
        """
        Test methods for getting single objects.
        """
        conn = self.conn

        # Test succesful get.
        obj = TestTable.get(conn, id=1)
        self.assert_(obj.firstname == u'Marité')

        # Test get failure.
        self.assertRaises(MormError, TestTable.get, conn, id=48337)


    def test_update(self):
        """
        Test methods for modifying existing data.
        """
        conn = self.conn

        #
        # Use an explicit encoder object to fill SQL statements.
        #
        curs = conn.cursor()
        enc = TestTable.encoder(lastname=u'Blais')
        curs.execute("UPDATE %s SET %s WHERE id = %%s" %
                     (enc.table(), enc.set()),
                     enc.values() + [1])
        conn.commit()

        # Check the new value.
        obj = TestTable.select(conn, 'WHERE id = %s', (1,)).next()
        self.assert_(obj.lastname == 'Blais')

        #
        # UPDATE on the encoder object.
        #
        enc = TestTable.encoder(lastname=u'Binoche')
        enc.update(conn, 'WHERE id = %s', (1,))
        conn.commit()

        # Check the new value.
        obj = TestTable.select(conn, 'WHERE id = %s', (1,)).next()
        self.assert_(obj.lastname == 'Binoche')

        #======================================================================\

        #
        # UPDATE on the table (the high-level, normal cases).
        #
        TestTable.update(conn,
                         'WHERE id = %s', (2,),
                         lastname=u'Depardieu',
                         religion='candomblé')
        conn.commit()

        # Check the new value.
        obj = TestTable.select(conn, 'WHERE id = %s', (2,)).next()
        self.assert_(obj.lastname == 'Depardieu')

        #======================================================================/


    def test_delete(self):
        """
        Test methods for deleting.
        """
        conn = self.conn

        it = TestTable.select(conn)
        self.assert_(len(it) == 3)

        #======================================================================\

        #
        # DELETE from the table.
        #
        TestTable.delete(conn,
                         'WHERE id = %s', (1,))
        it = TestTable.select(conn)
        self.assert_(len(it) == 2)

        TestTable.delete(conn)
        it = TestTable.select(conn)
        self.assert_(len(it) == 0)

        #======================================================================/


    def test_date(self):
        """
        Test storing and reading back a date.
        """
        conn = self.conn

        TestTable.insert(conn,
                         firstname=u'Gérard',
                         lastname=u'Depardieu',
                         religion='christian')
        conn.commit()

        # Check date type.
        import datetime
        today = datetime.date.today()

        TestTable.update(conn,
                         'WHERE lastname = %s', ('Depardieu',),
                         creation=today)
        conn.commit()

        it = TestTable.select(conn, 'WHERE lastname = %s', ('Depardieu',))
        obj = it.next()
        self.assert_(isinstance(obj.creation, datetime.date))


    def test_conversions(self):
        """
        Test some type conversions.
        """
        conn = self.conn

        # Check unicode string type.
        obj = TestTable.get(conn, id=4)
        self.assert_(isinstance(obj.firstname, unicode))
        self.assert_(obj.firstname == u'Gérard')
        self.assert_(isinstance(obj.lastname, unicode))
        self.assert_(obj.lastname == u'Depardieu')
        self.assert_(isinstance(obj.religion, str))
        self.assert_(obj.religion == u'christian'.encode('latin-1'))


    def test_sequence(self):
        """
        Test methods for encoding and for insertion.
        """
        conn = self.conn

        TestTable.insert(conn,
                         firstname=u'Rachel',
                         lastname=u'Lieblein-Harrod',
                         religion='jewish')
        conn.commit()

        #======================================================================\

        # Get the sequence number for the last insertion.
        seq = TestTable.getsequence(conn)

        obj = TestTable.select(conn, 'WHERE id = %s', (seq,)).next()
        self.assert_(obj.firstname == 'Rachel')

        #======================================================================/


    def test_create(self):
        """
        Test methods for creation (insertion and then getting at the object).
        """
        conn = self.conn

        #======================================================================\

        obj = TestTable.create(conn,
                               firstname=u'Hughes',
                               lastname=u'Leblanc',
                               religion='blackmagic')
        conn.commit()

        self.assert_(obj.lastname == 'Leblanc')

        #======================================================================/


    def test_multi_tables(self):
        """
        Test query on multiple tables with conversion.
        """
        conn = self.conn

        tables = (TestTable, TestTable2)
        curs = MormDecoder.do_select(conn, tables)
        dec = MormDecoder(tables, curs)

        TestTable2.insert(conn,
                          id=1,
                          motto=u"I don't want any, ok?")
        conn.commit()

        curs.execute("""
            SELECT firstname, lastname, motto FROM %s
              WHERE test1.id = test2.id
            """ % dec.tablenames())
        dec = MormDecoder(tables, curs)
        it = dec.iter(curs)
        assert it
        for o in it:
            assert o.firstname and o.lastname and o.motto
            assert isinstance(o.firstname, unicode)
            assert isinstance(o.motto, unicode)


def suite():
    thesuite = unittest.TestSuite()
    thesuite.addTest(TestMorm("test_insert"))
    thesuite.addTest(TestMorm("test_count"))
    thesuite.addTest(TestMorm("test_select"))
    thesuite.addTest(TestMorm("test_multi_tables"))
    thesuite.addTest(TestMorm("test_get"))
    thesuite.addTest(TestMorm("test_update"))
    thesuite.addTest(TestMorm("test_delete"))
    thesuite.addTest(TestMorm("test_date"))
    thesuite.addTest(TestMorm("test_conversions"))
    thesuite.addTest(TestMorm("test_sequence"))
    thesuite.addTest(TestMorm("test_create"))
    return thesuite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')



# -*- coding: utf-8 -*-
""" backup2swift.tests.test_utils """
import unittest
import sys
from backup2swift import utils as u
from backup2swift.tests import test_vars as v
if sys.version_info < (3, 0):
    from StringIO import StringIO
else:
    from io import StringIO


class UtilsTests(unittest.TestCase):
    """ Unit test of utils module. """

    def setUp(self):
        """ initialize unit test """
        self.capture = sys.stdout
        sys.stdout = StringIO()

    def tearDown(self):
        """ finalize unit test """
        sys.stdout = self.capture

    def test_list_data(self):
        """ unit test for list_data() """
        u.list_data(v.OBJECTS)
        self.assertEqual(v.OBJECT_TABLE,
                         sys.stdout.getvalue())

    def test_logging(self):
        """ unit test for logging """
        with self.assertRaises(SystemExit) as error:
            u.logging(3, 'test message')
        self.assertEqual(1, error.exception.code)
        self.assertEqual('test message\n', sys.stdout.getvalue())

    def test_get_columns_width(self):
        """ unit test for get_columns_width """
        self.assertListEqual(v.OBJECTS_ROW_WIDTH,
                             u.get_columns_width(v.HEADER_WIDTH,
                                                 v.OBJECTS_HEADER,
                                                 v.OBJECTS))

    def test_get_columns_width_fail(self):
        """ unit test for get_columns_width """
        self.assertNotEqual(v.DUMMY_ROW_WIDTH,
                            u.get_columns_width(v.HEADER_WIDTH,
                                                v.OBJECTS_HEADER,
                                                v.OBJECTS))

    def test_fqdn(self):
        """ unit test for FQDN """
        self.assertTrue(isinstance(u.FQDN, str))

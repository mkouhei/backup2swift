# -*- coding: utf-8 -*-
"""
    Copyright (C) 2013, 2014 Kouhei Maeda <mkouhei@palmtb.net>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import unittest
import sys
if sys.version_info < (3, 0):
    from StringIO import StringIO
else:
    from io import StringIO
from backup2swift import utils as u
from backup2swift.tests import test_vars as v


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

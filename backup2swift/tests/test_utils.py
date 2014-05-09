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

    def setUp(self):
        self.capture = sys.stdout
        sys.stdout = StringIO()

    def tearDown(self):
        sys.stdout = self.capture

    def test_list_data(self):
        u.list_data(v.objects)
        self.assertEqual(v.object_table,
                         sys.stdout.getvalue())

    def test_logging(self):
        with self.assertRaises(SystemExit) as e:
            u.logging(3, 'test message')
        self.assertEqual(1, e.exception.code)
        self.assertEqual('test message\n', sys.stdout.getvalue())

    def test_get_columns_width(self):
        self.assertListEqual(v.objects_row_width,
                             u.get_columns_width(v.header_width,
                                                 v.objects_header,
                                                 v.objects))

    def test_get_columns_width_fail(self):
        self.assertNotEqual(v.dummy_row_width,
                            u.get_columns_width(v.header_width,
                                                v.objects_header,
                                                v.objects))

    def test_FQDN(self):
        self.assertTrue(isinstance(u.FQDN, str))

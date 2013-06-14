# -*- coding: utf-8 -*-
"""
    Copyright (C) 2013 Kouhei Maeda <mkouhei@palmtb.net>

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
import os.path
sys.path.append(os.path.abspath('src'))
import backup2swift.utils as u
import backup2swift_tests.test_vars as v


class UtilsTests(unittest.TestCase):

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

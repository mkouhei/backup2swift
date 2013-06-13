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
from mock import patch
import swiftsc.client
import sys
import os.path
sys.path.append(os.path.abspath('src'))
import backup2swift.backup as b
import backup2swift_tests.test_vars as v


class BackupTests(unittest.TestCase):

    @patch('swiftsc.client.retrieve_token', return_value=(v.token, v.s_url))
    def setUp(self, m):
        self.b = b.Backup(v.auth_url, v.username, v.password)

    @patch('swiftsc.client.is_container', return_value=True)
    @patch('swiftsc.client.list_objects', return_value=v.objects)
    @patch('swiftsc.client.create_object', return_value=201)
    def test_backup(self, m1, m2, m3):
        self.assertEqual(self.b.backup("."), True)

    @patch('swiftsc.client.is_container', return_value=False)
    @patch('swiftsc.client.list_objects', return_value=v.objects)
    @patch('swiftsc.client.create_object', return_value=201)
    def test_backup_multiple_files(self, m1, m2, m3):
        self.assertEqual(self.b.backup(v.test_files), True)

    @patch('swiftsc.client.is_container', return_value=True)
    @patch('swiftsc.client.create_container', return_value=201)
    @patch('swiftsc.client.list_objects', return_value=v.objects)
    @patch('swiftsc.client.create_object', return_value=201)
    def test_backup_file_with_create_cont(self, m1, m2, m3, m4):
        self.assertEqual(self.b.backup_file("examples/bu2sw.conf"), True)

    @patch('swiftsc.client.is_container', return_value=True)
    @patch('swiftsc.client.create_container', return_value=202)
    @patch('swiftsc.client.list_objects', return_value=v.objects)
    @patch('swiftsc.client.create_object', return_value=201)
    def test_backup_file_with_created_cont(self, m1, m2, m3, m4):
        self.assertEqual(self.b.backup_file("examples/bu2sw.conf"), True)

    @patch('swiftsc.client.is_container', return_value=True)
    @patch('swiftsc.client.create_container', return_value=400)
    @patch('swiftsc.client.list_objects', return_value=v.objects)
    @patch('swiftsc.client.create_object', return_value=201)
    def test_backup_file_fail_create_cont(self, m1, m2, m3, m4):
        self.assertRaises(TypeError, self.b.backup_file("examples/bu2sw.conf"))

    @patch('swiftsc.client.is_container', return_value=True)
    @patch('swiftsc.client.create_container', return_value=202)
    @patch('swiftsc.client.list_objects', return_value=v.objects)
    @patch('swiftsc.client.create_object', return_value=201)
    def test_backup_file_create_object(self, m1, m2, m3, m4):
        self.assertEqual(self.b.backup_file("examples/bu2sw.conf"), True)

    @patch('swiftsc.client.is_container', return_value=True)
    @patch('swiftsc.client.create_container', return_value=201)
    @patch('swiftsc.client.list_objects', return_value=v.objects)
    @patch('swiftsc.client.create_object', return_value=202)
    def test_backup_file_override(self, m1, m2, m3, m4):
        self.assertEqual(self.b.backup_file("examples/bu2sw.conf"), True)

    @patch('swiftsc.client.is_container', return_value=True)
    @patch('swiftsc.client.create_container', return_value=201)
    @patch('swiftsc.client.list_objects', return_value=v.objects)
    @patch('swiftsc.client.create_object', return_value=400)
    def test_backup_file_fail(self, m1, m2, m3, m4):
        self.assertRaises(RuntimeError, self.b.backup_file,
                          "examples/bu2sw.conf")

    @patch('swiftsc.client.copy_object', return_value=201)
    @patch('swiftsc.client.create_object', return_value=201)
    @patch('swiftsc.client.delete_object', return_value=204)
    def test_rotate(self, m1, m2, m3):
        self.assertEqual(self.b.rotate(v.test_file, v.object_name,
                                       v.objects_name_l), True)

    @patch('swiftsc.client.copy_object', return_value=400)
    def test_rotate_fail_copy(self, m1):
        self.assertRaises(RuntimeError, self.b.rotate,
                          v.test_file, v.object_name, v.objects_name_l)

    @patch('swiftsc.client.copy_object', return_value=201)
    @patch('swiftsc.client.create_object', return_value=400)
    def test_rotate_fail_create(self, m1, m2):
        self.assertRaises(RuntimeError, self.b.rotate, v.test_file,
                          v.object_name, v.objects_name_l)

    # ToDo should add raise exception when delete object?
    @patch('swiftsc.client.copy_object', return_value=201)
    @patch('swiftsc.client.create_object', return_value=201)
    @patch('swiftsc.client.delete_object', return_value=400)
    def test_rotate_fail_delete(self, m1, m2, m3):
        self.assertEqual(self.b.rotate(v.test_file, v.object_name,
                                       v.objects_name_l), True)

    @patch('swiftsc.client.is_container', return_value=True)
    @patch('swiftsc.client.list_objects', return_value=v.objects)
    def test_retrieve_backup_data_list(self, m1, m2):
        self.assertEqual(self.b.retrieve_backup_data_list(),
                         v.objects_name_l)
        self.assertEqual(self.b.retrieve_backup_data_list(True),
                         v.objects)

    @patch('swiftsc.client.is_container', return_value=False)
    def test_retrieve_backup_data_list(self, m):
        self.assertEqual(self.b.retrieve_backup_data_list(),
                         [])

    @patch('swiftsc.client.is_container', return_value=True)
    @patch('swiftsc.client.is_object', return_value=True)
    @patch('swiftsc.client.delete_object', return_value=204)
    def test_delete_backup_data(self, m1, m2, m3):
        self.assertEqual(self.b.delete_backup_data("dummy"), True)

    @patch('swiftsc.client.is_container', return_value=True)
    @patch('swiftsc.client.is_object', return_value=True)
    @patch('swiftsc.client.delete_object', return_value=204)
    def test_delete_backup_multiple_data(self, m1, m2, m3):
        self.assertEqual(self.b.delete_backup_data(v.objects_name), None)

    @patch('swiftsc.client.is_container', return_value=False)
    def test_delete_backup_data_without_container(self, m):
        self.assertRaises(RuntimeError, self.b.delete_backup_data, "dummy")

    @patch('swiftsc.client.is_container', return_value=True)
    @patch('swiftsc.client.is_object', return_value=False)
    def test_delete_backup_data_without_object(self, m1, m2):
        self.assertRaises(RuntimeError, self.b.delete_backup_data, "dummy")

    @patch('swiftsc.client.is_container', return_value=True)
    @patch('swiftsc.client.is_object', return_value=True)
    @patch('swiftsc.client.delete_object', return_value=False)
    def test_delete_backup_data_runtime_error(self, m1, m2, m3):
        self.assertRaises(RuntimeError, self.b.delete_backup_data, "dummy")

    @patch('swiftsc.client.is_container', return_value=True)
    @patch('swiftsc.client.is_object', return_value=True)
    @patch('swiftsc.client.retrieve_object', return_value=(True, ''))
    def test_retrieve_backup_data(self, m1, m2, m3):
        self.assertEqual(self.b.retrieve_backup_data("dummy"), None)

    @patch('swiftsc.client.is_container', return_value=False)
    def test_retrieve_backup_data_without_container(self, m):
        self.assertRaises(RuntimeError, self.b.retrieve_backup_data, "dummy")

    @patch('swiftsc.client.is_container', return_value=True)
    @patch('swiftsc.client.is_object', return_value=False)
    def test_retrieve_backup_data_without_object(self, m1, m2):
        self.assertRaises(RuntimeError, self.b.retrieve_backup_data, "dummy")

    @patch('swiftsc.client.is_container', return_value=True)
    @patch('swiftsc.client.is_object', return_value=True)
    @patch('swiftsc.client.retrieve_object', return_value=(False, ''))
    def test_retrieve_backup_data(self, m1, m2, m3):
        self.assertRaises(RuntimeError, self.b.retrieve_backup_data, "dummy")

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
from mock import patch
from backup2swift import backup as bkup
from backup2swift.tests import test_vars as v


class BackupTests(unittest.TestCase):
    """ test module of backup """

    @patch('swiftsc.client.retrieve_token', return_value=(v.TOKEN, v.S_URL))
    def setUp(self, _mock1):
        """ initialize """
        self.bkup = bkup.Backup(v.AUTH_URL, v.USERNAME, v.PASSWORD)

    @patch('swiftsc.client.is_container', return_value=True)
    @patch('swiftsc.client.list_objects', return_value=v.OBJECTS)
    @patch('swiftsc.client.create_object', return_value=201)
    def test_backup(self, _mock1, _mock2, _mock3):
        """ unit test for backup """
        self.assertEqual(self.bkup.backup("."), True)

    @patch('swiftsc.client.is_container', return_value=False)
    @patch('swiftsc.client.list_objects', return_value=v.OBJECTS)
    @patch('swiftsc.client.create_object', return_value=201)
    def test_backup_multiple_files(self, _mock1, _mock2, _mock3):
        """ unit test for backup multiple files """
        self.assertEqual(self.bkup.backup(v.TEST_FILES), True)

    @patch('swiftsc.client.is_container', return_value=True)
    @patch('swiftsc.client.create_container', return_value=201)
    @patch('swiftsc.client.list_objects', return_value=v.OBJECTS)
    @patch('swiftsc.client.create_object', return_value=201)
    def test_backup_file_create_cont(self, _mock1, _mock2, _mock3, _mock4):
        """ unit test for create container and backup file """
        self.assertEqual(self.bkup.backup_file("examples/bu2sw.conf"), True)

    @patch('swiftsc.client.is_container', return_value=True)
    @patch('swiftsc.client.create_container', return_value=202)
    @patch('swiftsc.client.list_objects', return_value=v.OBJECTS)
    @patch('swiftsc.client.create_object', return_value=201)
    def test_backup_file_created_cont(self, _mock1, _mock2, _mock3, _mock4):
        """ unit test for backup file to existed contianer """
        self.assertEqual(self.bkup.backup_file("examples/bu2sw.conf"), True)

    @patch('swiftsc.client.is_container', return_value=False)
    @patch('swiftsc.client.create_container', return_value=400)
    @patch('swiftsc.client.list_objects', return_value=v.OBJECTS)
    @patch('swiftsc.client.create_object', return_value=201)
    def test_backup_failed_create_cont(self, _mock1, _mock2, _mock3, _mock4):
        """ unit test for backup file when failed to create contianer """
        self.assertRaises(RuntimeError,
                          self.bkup.backup_file,
                          "examples/bu2sw.conf")

    @patch('swiftsc.client.is_container', return_value=True)
    @patch('swiftsc.client.create_container', return_value=202)
    @patch('swiftsc.client.list_objects', return_value=v.OBJECTS)
    @patch('swiftsc.client.create_object', return_value=201)
    def test_backup_file_create_object(self, _mock1, _mock2, _mock3, _mock4):
        """ unit test for backup file and create object """
        self.assertEqual(self.bkup.backup_file("examples/bu2sw.conf"), True)

    @patch('swiftsc.client.is_container', return_value=True)
    @patch('swiftsc.client.create_container', return_value=202)
    @patch('swiftsc.client.list_objects', return_value=v.OBJECTS)
    @patch('swiftsc.client.create_object', return_value=201)
    def test_backup_creating_from_stdin(self, _mock1, _mock2, _mock3, _mock4):
        """ unit test for backup file and create object form stdin """
        test_data = open("examples/bu2sw.conf", 'rb', buffering=0)
        self.assertEqual(self.bkup.backup_file("bu2sw.conf",
                                               test_data), True)
        test_data.close()

    @patch('swiftsc.client.is_container', return_value=True)
    @patch('swiftsc.client.create_container', return_value=201)
    @patch('swiftsc.client.list_objects', return_value=v.OBJECTS)
    @patch('swiftsc.client.create_object', return_value=202)
    def test_backup_file_override(self, _mock1, _mock2, _mock3, _mock4):
        """ unit test for backup file and override object  """
        self.assertEqual(self.bkup.backup_file("examples/bu2sw.conf"), True)

    @patch('swiftsc.client.is_container', return_value=True)
    @patch('swiftsc.client.create_container', return_value=201)
    @patch('swiftsc.client.list_objects', return_value=v.OBJECTS)
    @patch('swiftsc.client.create_object', return_value=400)
    def test_backup_file_fail(self, _mock1, _mock2, _mock3, _mock4):
        """ unit test for fail backup file """
        self.assertRaises(RuntimeError, self.bkup.backup_file,
                          "examples/bu2sw.conf")

    @patch('swiftsc.client.copy_object', return_value=201)
    @patch('swiftsc.client.create_object', return_value=201)
    @patch('swiftsc.client.delete_object', return_value=204)
    def test_rotate(self, _mock1, _mock2, _mock3):
        """ unit test for rotate object """
        self.assertEqual(self.bkup.rotate(v.TEST_FILE, v.OBJECT_NAME,
                                          v.OBJECTS_NAME_L), True)

    @patch('swiftsc.client.copy_object', return_value=400)
    def test_rotate_fail_copy(self, _mock1):
        """ unit test for fail to copy object """
        self.assertRaises(RuntimeError, self.bkup.rotate,
                          v.TEST_FILE, v.OBJECT_NAME, v.OBJECTS_NAME_L)

    @patch('swiftsc.client.copy_object', return_value=201)
    @patch('swiftsc.client.create_object', return_value=400)
    def test_rotate_fail_create(self, _mock1, _mock2):
        """ unit test for fail to rotate """
        self.assertRaises(RuntimeError, self.bkup.rotate, v.TEST_FILE,
                          v.OBJECT_NAME, v.OBJECTS_NAME_L)

    # ToDo should add raise exception when delete object?
    @patch('swiftsc.client.copy_object', return_value=201)
    @patch('swiftsc.client.create_object', return_value=201)
    @patch('swiftsc.client.delete_object', return_value=400)
    def test_rotate_fail_delete(self, _mock1, _mock2, _mock3):
        """ unit test for fail to delete """
        self.assertEqual(self.bkup.rotate(v.TEST_FILE, v.OBJECT_NAME,
                                          v.OBJECTS_NAME_L), True)

    @patch('swiftsc.client.is_container', return_value=True)
    @patch('swiftsc.client.list_objects', return_value=v.OBJECTS)
    def test_retrieve_backup_data_list(self, _mock1, _mock2):
        """ unit test for retrieving backup data list """
        self.assertEqual(self.bkup.retrieve_backup_data_list(),
                         v.OBJECTS_NAME_L)
        self.assertEqual(self.bkup.retrieve_backup_data_list(True),
                         v.OBJECTS)

    @patch('swiftsc.client.is_container', return_value=False)
    def test_retrieve_backup_nonedata(self, _mock1):
        """ unit test for retrieving backup none data list """
        self.assertEqual(self.bkup.retrieve_backup_data_list(),
                         [])

    @patch('swiftsc.client.is_container', return_value=True)
    @patch('swiftsc.client.is_object', return_value=True)
    @patch('swiftsc.client.delete_object', return_value=204)
    def test_delete_backup_data(self, _mock1, _mock2, _mock3):
        """ unit test for delete object """
        self.assertEqual(self.bkup.delete_backup_data("dummy"), True)

    @patch('swiftsc.client.is_container', return_value=True)
    @patch('swiftsc.client.is_object', return_value=True)
    @patch('swiftsc.client.delete_object', return_value=204)
    def test_delete_multiple_backups(self, _mock1, _mock2, _mock3):
        """ unit test for delete multiple object """
        self.assertEqual(self.bkup.delete_backup_data(v.OBJECTS_NAME), None)

    @patch('swiftsc.client.is_container', return_value=False)
    def test_delete_backups_nocontainer(self, _mock1):
        """ unit test for delete object without container """
        self.assertRaises(RuntimeError, self.bkup.delete_backup_data, "dummy")

    @patch('swiftsc.client.is_container', return_value=True)
    @patch('swiftsc.client.is_object', return_value=False)
    def test_delete_backups_noobject(self, _mock1, _mock2):
        """ unit test for delete backup data without object """
        self.assertRaises(RuntimeError, self.bkup.delete_backup_data, "dummy")

    @patch('swiftsc.client.is_container', return_value=True)
    @patch('swiftsc.client.is_object', return_value=True)
    @patch('swiftsc.client.delete_object', return_value=False)
    def test_delete_backups_failed(self, _mock1, _mock2, _mock3):
        """ unit test for fail to delete object """
        self.assertRaises(RuntimeError, self.bkup.delete_backup_data, "dummy")

    @patch('swiftsc.client.is_container', return_value=True)
    @patch('swiftsc.client.is_object', return_value=True)
    @patch('swiftsc.client.retrieve_object', return_value=(True, ''))
    def test_retrieve_backup_data(self, _mock1, _mock2, _mock3):
        """ unit test for retrieving backup data """
        self.assertEqual(self.bkup.retrieve_backup_data("dummy"), None)

    @patch('swiftsc.client.is_container', return_value=False)
    def test_retrieving_no_container(self, _mock1):
        """ unit test for retrieving backup data without container """
        self.assertRaises(RuntimeError,
                          self.bkup.retrieve_backup_data, "dummy")

    @patch('swiftsc.client.is_container', return_value=True)
    @patch('swiftsc.client.is_object', return_value=False)
    def test_retrieve_backups_no_object(self, _mock1, _mock2):
        """ unit test for retrieving backup data without object """
        self.assertRaises(RuntimeError,
                          self.bkup.retrieve_backup_data, "dummy")

    @patch('swiftsc.client.is_container', return_value=True)
    @patch('swiftsc.client.is_object', return_value=True)
    @patch('swiftsc.client.retrieve_object', return_value=(False, ''))
    def test_retrieve_backup_data_fail(self, _mock1, _mock2, _mock3):
        """ unit test for fail to retrieving backup data """
        self.assertRaises(RuntimeError,
                          self.bkup.retrieve_backup_data, "dummy")

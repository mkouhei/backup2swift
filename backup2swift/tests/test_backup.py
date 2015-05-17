# -*- coding: utf-8 -*-
""" backup2swift.tests.test_backup """
import unittest
import os
from datetime import datetime
import requests_mock
from backup2swift import backup as bkup
from backup2swift.tests import test_vars as v


def timestamp():
    """ timestamp for ratation """
    return datetime.now().strftime('%Y%m%d-%H%M%S')


def dest_obj(name):
    """ dest object name for copy """
    return '%s_%s' % (name, timestamp())


class BackupTests(unittest.TestCase):
    """ test module of backup """

    @requests_mock.Mocker()
    def setUp(self, _mock):
        """initialize"""
        _mock.get(v.AUTH_URL,
                  headers={'X-Auth-Token': v.TOKEN,
                           'X-Storage-URL': v.STORAGE_URL},
                  status_code=200)
        self.bkup = bkup.Backup(v.AUTH_URL,
                                v.USERNAME,
                                v.PASSWORD,
                                container_name=v.CONTAINER_NAME)

    def tearDown(self):
        if os.path.isfile(v.OBJECT_NAME):
            os.remove(v.OBJECT_NAME)

    @requests_mock.Mocker()
    def test_backup(self, _mock):
        """unit test backup"""
        _mock.head('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                   status_code=204)
        _mock.get('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                  json=v.OBJECTS,
                  status_code=200)
        dest_file = '%s_%s' % (v.OBJECT_NAME, timestamp())
        _mock.put('%s/%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME, dest_file),
                  status_code=201)
        _mock.put('%s/%s/%s' % (v.STORAGE_URL,
                                v.CONTAINER_NAME,
                                v.OBJECT_NAME),
                  status_code=201)
        self.assertTrue(
            self.bkup.backup("backup2swift/tests/data/%s" % v.OBJECT_NAME))

    @requests_mock.Mocker()
    def test_backup_from_stdin(self, _mock):
        """unit test backup from stdin"""
        _mock.head('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                   status_code=204)
        _mock.get('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                  json=[],
                  status_code=200)
        _mock.put('%s/%s/%s' % (v.STORAGE_URL,
                                v.CONTAINER_NAME,
                                v.OBJECT_NAME),
                  status_code=201)
        data = open("backup2swift/tests/data/sample.txt", "rb", buffering=0)
        self.assertTrue(
            self.bkup.backup_file(v.OBJECT_NAME, data))
        data.close()

    def test_backup_multiple_files(self):
        """unit test for backup multiple files

        but not work backup_file
        why utils.multiprocess has no multiprocessing.Process.join().
        """
        self.assertEqual(self.bkup.backup(v.TEST_FILES), None)

    @requests_mock.Mocker()
    def test_backup_with_new_container(self, _mock):
        """unit test backup and create container"""
        _mock.head('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                   status_code=404)
        _mock.put('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                  status_code=201)
        _mock.get('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                  json=[],
                  status_code=200)
        _mock.put('%s/%s/%s' % (v.STORAGE_URL,
                                v.CONTAINER_NAME,
                                v.OBJECT_NAME),
                  status_code=201)
        self.assertTrue(
            self.bkup.backup("backup2swift/tests/data/%s" % v.OBJECT_NAME))

    @requests_mock.Mocker()
    def test_fail_create_container(self, _mock):
        """unit test fail create container"""
        _mock.head('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                   status_code=404)
        _mock.put('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                  status_code=400)
        self.assertRaises(RuntimeError,
                          self.bkup.backup,
                          "backup2swift/tests/data/%s" % v.OBJECT_NAME)

    @requests_mock.Mocker()
    def test_fail_copy(self, _mock):
        """unit test fail copy backup"""
        _mock.head('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                   status_code=204)
        _mock.get('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                  json=v.OBJECTS,
                  status_code=200)
        dest_file = '%s_%s' % (v.OBJECT_NAME, timestamp())
        _mock.put('%s/%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME, dest_file),
                  status_code=400)
        self.assertRaises(RuntimeError,
                          self.bkup.backup,
                          "backup2swift/tests/data/%s" % v.OBJECT_NAME)

    @requests_mock.Mocker()
    def test_fail_rotate(self, _mock):
        """unit test fail rotate backup"""
        _mock.head('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                   status_code=204)
        _mock.get('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                  json=v.OBJECTS,
                  status_code=200)
        dest_file = '%s_%s' % (v.OBJECT_NAME, timestamp())
        _mock.put('%s/%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME, dest_file),
                  status_code=201)
        _mock.put('%s/%s/%s' % (v.STORAGE_URL,
                                v.CONTAINER_NAME,
                                v.OBJECT_NAME),
                  status_code=400)
        self.assertRaises(RuntimeError,
                          self.bkup.backup,
                          "backup2swift/tests/data/%s" % v.OBJECT_NAME)

    @requests_mock.Mocker()
    def test_delete_backup(self, _mock):
        """unit test delete backup"""
        _mock.head('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                   status_code=204)
        _mock.get('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                  json=v.OBJECTS,
                  status_code=200)
        _mock.head('%s/%s/%s' % (v.STORAGE_URL,
                                 v.CONTAINER_NAME,
                                 v.OBJECT_NAME),
                   status_code=204)
        _mock.delete('%s/%s/%s' % (v.STORAGE_URL,
                                   v.CONTAINER_NAME,
                                   v.OBJECT_NAME),
                     status_code=204)
        self.assertTrue(self.bkup.delete_backup_data(v.OBJECT_NAME))

    @requests_mock.Mocker()
    def test_fail_delete_backup(self, _mock):
        """unit test fail delete backup"""
        _mock.head('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                   status_code=204)
        _mock.get('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                  json=v.OBJECTS,
                  status_code=200)
        _mock.head('%s/%s/%s' % (v.STORAGE_URL,
                                 v.CONTAINER_NAME,
                                 v.OBJECT_NAME),
                   status_code=204)
        _mock.delete('%s/%s/%s' % (v.STORAGE_URL,
                                   v.CONTAINER_NAME,
                                   v.OBJECT_NAME),
                     status_code=400)
        self.assertRaises(RuntimeError,
                          self.bkup.delete_backup_data,
                          v.OBJECT_NAME)

    @requests_mock.Mocker()
    def test_delete_multiple_backup(self, _mock):
        """unit test delete multiple backup"""
        _mock.head('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                   status_code=204)
        _mock.get('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                  json=v.OBJECTS,
                  status_code=200)
        for i in v.OBJECTS_NAME:
            _mock.head('%s/%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME, i),
                       status_code=204)
            _mock.delete('%s/%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME, i),
                         status_code=400)
        self.assertTrue(self.bkup.delete_backup_data, v.OBJECTS_NAME)

    @requests_mock.Mocker()
    def test_delete_object_no_container(self, _mock):
        """unit test delete no container"""
        _mock.head('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                   status_code=404)
        self.assertRaises(RuntimeError,
                          self.bkup.delete_backup_data,
                          v.OBJECT_NAME)

    @requests_mock.Mocker()
    def test_delete_noexist_backup(self, _mock):
        """unit test delete no object"""
        _mock.head('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                   status_code=204)
        _mock.get('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                  json=v.OBJECTS,
                  status_code=200)
        _mock.head('%s/%s/%s' % (v.STORAGE_URL,
                                 v.CONTAINER_NAME,
                                 v.OBJECT_NAME),
                   status_code=404)
        self.assertRaises(RuntimeError,
                          self.bkup.delete_backup_data,
                          v.OBJECT_NAME)

    @requests_mock.Mocker()
    def test_fail_delete_multiple(self, _mock):
        """unit test fail delete multiple objects"""
        _mock.head('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                   status_code=204)
        _mock.get('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                  json=v.OBJECTS,
                  status_code=200)
        for i in v.OBJECTS_NAME:
            _mock.head('%s/%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME, i),
                       status_code=204)
            _mock.delete('%s/%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME, i),
                         status_code=400)
        self.assertRaises(RuntimeError,
                          self.bkup.delete_backup_data,
                          v.OBJECTS_NAME)

    @requests_mock.Mocker()
    def test_retrieve_backup_data(self, _mock):
        """unit test retrieve a object"""
        _mock.head('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                   status_code=204)
        _mock.get('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                  json=v.OBJECTS,
                  status_code=200)
        _mock.head('%s/%s/%s' % (v.STORAGE_URL,
                                 v.CONTAINER_NAME,
                                 v.OBJECT_NAME),
                   status_code=204)
        _mock.get('%s/%s/%s' % (v.STORAGE_URL,
                                v.CONTAINER_NAME,
                                v.OBJECT_NAME),
                  status_code=200)
        self.assertTrue(self.bkup.retrieve_backup_data(v.OBJECT_NAME))

    @requests_mock.Mocker()
    def test_retrieve_with_filename(self, _mock):
        """unit test retrieve a object with filename"""
        _mock.head('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                   status_code=204)
        _mock.get('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                  json=v.OBJECTS,
                  status_code=200)
        _mock.head('%s/%s/%s' % (v.STORAGE_URL,
                                 v.CONTAINER_NAME,
                                 v.OBJECT_NAME),
                   status_code=204)
        _mock.get('%s/%s/%s' % (v.STORAGE_URL,
                                v.CONTAINER_NAME,
                                v.OBJECT_NAME),
                  status_code=200)
        self.assertTrue(self.bkup.retrieve_backup_data(v.OBJECT_NAME,
                                                       v.OBJECT_NAME))

    @requests_mock.Mocker()
    def test_retrieve_no_container(self, _mock):
        """unit test retrieve a object no container"""
        _mock.head('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                   status_code=404)
        self.assertRaises(RuntimeError,
                          self.bkup.retrieve_backup_data,
                          v.OBJECT_NAME)

    @requests_mock.Mocker()
    def test_retrieve_backup_nodata(self, _mock):
        """unit test retrieve no object"""
        _mock.head('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                   status_code=204)
        _mock.get('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                  json=v.OBJECTS,
                  status_code=200)
        _mock.head('%s/%s/%s' % (v.STORAGE_URL,
                                 v.CONTAINER_NAME,
                                 v.OBJECT_NAME),
                   status_code=404)
        self.assertRaises(RuntimeError,
                          self.bkup.retrieve_backup_data,
                          v.OBJECT_NAME)

    @requests_mock.Mocker()
    def test_retrieve_fail_backup_data(self, _mock):
        """unit test fail retrieve a object"""
        _mock.head('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                   status_code=204)
        _mock.get('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                  json=v.OBJECTS,
                  status_code=200)
        _mock.head('%s/%s/%s' % (v.STORAGE_URL,
                                 v.CONTAINER_NAME,
                                 v.OBJECT_NAME),
                   status_code=204)
        _mock.get('%s/%s/%s' % (v.STORAGE_URL,
                                v.CONTAINER_NAME,
                                v.OBJECT_NAME),
                  status_code=400)
        self.assertRaises(RuntimeError,
                          self.bkup.retrieve_backup_data,
                          v.OBJECT_NAME)

    @requests_mock.Mocker()
    def test_retrieve_multiple_backup(self, _mock):
        """unit test retrieve multiple objects"""
        _mock.head('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                   status_code=204)
        _mock.get('%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                  json=v.OBJECTS,
                  status_code=200)
        for i in v.OBJECTS_NAME:
            _mock.head('%s/%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME, i),
                       status_code=204)
            _mock.get('%s/%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME, i),
                      status_code=200)
        self.assertTrue(self.bkup.delete_backup_data, v.OBJECTS_NAME)

# -*- coding: utf-8 -*-
""" backup2swift.tests.test_backup """
import unittest
import json
import os
from datetime import datetime
import httpretty
from httpretty import HTTPretty, httprettified
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

    @httprettified
    def setUp(self):
        """ initialize """
        HTTPretty.register_uri(HTTPretty.GET,
                               v.AUTH_URL,
                               adding_headers={
                                   'X-Auth-Token': v.TOKEN,
                                   'X-Storage-URL': v.STORAGE_URL})

        self.bkup = bkup.Backup(v.AUTH_URL,
                                v.USERNAME,
                                v.PASSWORD,
                                container_name=v.CONTAINER_NAME)

    def tearDown(self):
        if os.path.isfile(v.OBJECT_NAME):
            os.remove(v.OBJECT_NAME)
        httpretty.disable()

    @httprettified
    def test_backup(self):
        """ unit test backup """
        HTTPretty.register_uri(HTTPretty.HEAD,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               status=204)
        HTTPretty.register_uri(HTTPretty.GET,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               status=200,
                               body=json.dumps(v.OBJECTS))
        dest_file = '%s_%s' % (v.OBJECT_NAME, timestamp())
        HTTPretty.register_uri(HTTPretty.PUT,
                               '%s/%s/%s' % (v.STORAGE_URL,
                                             v.CONTAINER_NAME,
                                             dest_file),
                               status=201)
        HTTPretty.register_uri(HTTPretty.PUT,
                               '%s/%s/%s' % (v.STORAGE_URL,
                                             v.CONTAINER_NAME,
                                             v.OBJECT_NAME),
                               status=201)
        self.assertTrue(
            self.bkup.backup("backup2swift/tests/data/%s" % v.OBJECT_NAME))

    @httprettified
    def test_backup_multiple_files(self):
        """ unit test for backup multiple files, but not work backup_file
        why utils.multiprocess has no multiprocessing.Process.join().
        """
        self.assertEqual(self.bkup.backup(v.TEST_FILES), None)

    @httprettified
    def test_backup_with_new_container(self):
        """ unit test backup and create container """
        HTTPretty.register_uri(HTTPretty.HEAD,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               status=404)
        HTTPretty.register_uri(HTTPretty.PUT,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               status=201)
        HTTPretty.register_uri(HTTPretty.GET,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               body=json.dumps([]),
                               status=200)
        HTTPretty.register_uri(HTTPretty.PUT,
                               '%s/%s/%s' % (v.STORAGE_URL,
                                             v.CONTAINER_NAME,
                                             v.OBJECT_NAME),
                               status=201)
        self.assertTrue(
            self.bkup.backup("backup2swift/tests/data/%s" % v.OBJECT_NAME))

    @httprettified
    def test_fail_create_container(self):
        """ unit test fail create container """
        HTTPretty.register_uri(HTTPretty.HEAD,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               status=404)
        HTTPretty.register_uri(HTTPretty.PUT,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               status=400)
        self.assertRaises(RuntimeError,
                          self.bkup.backup,
                          "backup2swift/tests/data/%s" % v.OBJECT_NAME)

    @httprettified
    def test_fail_copy(self):
        """ unit test fail copy backup """
        HTTPretty.register_uri(HTTPretty.HEAD,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               status=204)
        HTTPretty.register_uri(HTTPretty.GET,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               status=200,
                               body=json.dumps(v.OBJECTS))
        dest_file = '%s_%s' % (v.OBJECT_NAME, timestamp())
        HTTPretty.register_uri(HTTPretty.PUT,
                               '%s/%s/%s' % (v.STORAGE_URL,
                                             v.CONTAINER_NAME,
                                             dest_file),
                               status=400)
        self.assertRaises(RuntimeError,
                          self.bkup.backup,
                          "backup2swift/tests/data/%s" % v.OBJECT_NAME)

    @httprettified
    def test_fail_rotate(self):
        """ unit test fail rotate backup """
        HTTPretty.register_uri(HTTPretty.HEAD,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               status=204)
        HTTPretty.register_uri(HTTPretty.GET,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               status=200,
                               body=json.dumps(v.OBJECTS))
        dest_file = '%s_%s' % (v.OBJECT_NAME, timestamp())
        HTTPretty.register_uri(HTTPretty.PUT,
                               '%s/%s/%s' % (v.STORAGE_URL,
                                             v.CONTAINER_NAME,
                                             dest_file),
                               status=201)
        HTTPretty.register_uri(HTTPretty.PUT,
                               '%s/%s/%s' % (v.STORAGE_URL,
                                             v.CONTAINER_NAME,
                                             v.OBJECT_NAME),
                               status=400)
        self.assertRaises(RuntimeError,
                          self.bkup.backup,
                          "backup2swift/tests/data/%s" % v.OBJECT_NAME)

    @httprettified
    def test_delete_backup(self):
        """ unit test delete backup """
        HTTPretty.register_uri(HTTPretty.HEAD,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               status=204)
        HTTPretty.register_uri(HTTPretty.GET,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               status=200,
                               body=json.dumps(v.OBJECTS))
        HTTPretty.register_uri(HTTPretty.HEAD,
                               '%s/%s/%s' % (v.STORAGE_URL,
                                             v.CONTAINER_NAME,
                                             v.OBJECT_NAME),
                               status=204)
        HTTPretty.register_uri(HTTPretty.DELETE,
                               '%s/%s/%s' % (v.STORAGE_URL,
                                             v.CONTAINER_NAME,
                                             v.OBJECT_NAME),
                               status=204)
        self.assertTrue(self.bkup.delete_backup_data(v.OBJECT_NAME))

    @httprettified
    def test_fail_delete_backup(self):
        """ unit test fail delete backup """
        HTTPretty.register_uri(HTTPretty.HEAD,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               status=204)
        HTTPretty.register_uri(HTTPretty.GET,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               status=200,
                               body=json.dumps(v.OBJECTS))
        HTTPretty.register_uri(HTTPretty.HEAD,
                               '%s/%s/%s' % (v.STORAGE_URL,
                                             v.CONTAINER_NAME,
                                             v.OBJECT_NAME),
                               status=204)
        HTTPretty.register_uri(HTTPretty.DELETE,
                               '%s/%s/%s' % (v.STORAGE_URL,
                                             v.CONTAINER_NAME,
                                             v.OBJECT_NAME),
                               status=400)
        self.assertRaises(RuntimeError,
                          self.bkup.delete_backup_data,
                          v.OBJECT_NAME)

    @httprettified
    def test_delete_multiple_backup(self):
        """ unit test delete multiple backup """
        HTTPretty.register_uri(HTTPretty.HEAD,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               status=204)
        HTTPretty.register_uri(HTTPretty.GET,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               status=200,
                               body=json.dumps(v.OBJECTS))
        for i in v.OBJECTS_NAME:
            HTTPretty.register_uri(HTTPretty.HEAD,
                                   '%s/%s/%s' % (v.STORAGE_URL,
                                                 v.CONTAINER_NAME,
                                                 i),
                                   status=204)
            HTTPretty.register_uri(HTTPretty.DELETE,
                                   '%s/%s/%s' % (v.STORAGE_URL,
                                                 v.CONTAINER_NAME,
                                                 i),
                                   status=400)
        self.assertTrue(self.bkup.delete_backup_data, v.OBJECTS_NAME)

    @httprettified
    def test_delete_object_no_container(self):
        """ unit test delete no container """
        HTTPretty.register_uri(HTTPretty.HEAD,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               status=404)
        self.assertRaises(RuntimeError,
                          self.bkup.delete_backup_data,
                          v.OBJECT_NAME)

    @httprettified
    def test_delete_noexist_backup(self):
        """ unit test delete no object """
        HTTPretty.register_uri(HTTPretty.HEAD,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               status=204)
        HTTPretty.register_uri(HTTPretty.GET,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               status=200,
                               body=json.dumps(v.OBJECTS))
        HTTPretty.register_uri(HTTPretty.HEAD,
                               '%s/%s/%s' % (v.STORAGE_URL,
                                             v.CONTAINER_NAME,
                                             v.OBJECT_NAME),
                               status=404)
        self.assertRaises(RuntimeError,
                          self.bkup.delete_backup_data,
                          v.OBJECT_NAME)

    @httprettified
    def test_fail_delete_multiple(self):
        """ unit test fail delete multiple objects """
        HTTPretty.register_uri(HTTPretty.HEAD,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               status=204)
        HTTPretty.register_uri(HTTPretty.GET,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               status=200,
                               body=json.dumps(v.OBJECTS))
        for i in v.OBJECTS_NAME:
            HTTPretty.register_uri(HTTPretty.HEAD,
                                   '%s/%s/%s' % (v.STORAGE_URL,
                                                 v.CONTAINER_NAME,
                                                 i),
                                   status=204)
            HTTPretty.register_uri(HTTPretty.DELETE,
                                   '%s/%s/%s' % (v.STORAGE_URL,
                                                 v.CONTAINER_NAME,
                                                 i),
                                   status=400)
        self.assertRaises(RuntimeError,
                          self.bkup.delete_backup_data,
                          v.OBJECTS_NAME)

    @httprettified
    def test_retrieve_backup_data(self):
        """ unit test retrieve a object """
        HTTPretty.register_uri(HTTPretty.HEAD,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               status=204)
        HTTPretty.register_uri(HTTPretty.GET,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               status=200,
                               body=json.dumps(v.OBJECTS))
        HTTPretty.register_uri(HTTPretty.HEAD,
                               '%s/%s/%s' % (v.STORAGE_URL,
                                             v.CONTAINER_NAME,
                                             v.OBJECT_NAME),
                               status=204)
        HTTPretty.register_uri(HTTPretty.GET,
                               '%s/%s/%s' % (v.STORAGE_URL,
                                             v.CONTAINER_NAME,
                                             v.OBJECT_NAME),
                               status=200)
        self.assertTrue(self.bkup.retrieve_backup_data(v.OBJECT_NAME))

    @httprettified
    def test_retrieve_with_filename(self):
        """ unit test retrieve a object with filename """
        HTTPretty.register_uri(HTTPretty.HEAD,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               status=204)
        HTTPretty.register_uri(HTTPretty.GET,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               status=200,
                               body=json.dumps(v.OBJECTS))
        HTTPretty.register_uri(HTTPretty.HEAD,
                               '%s/%s/%s' % (v.STORAGE_URL,
                                             v.CONTAINER_NAME,
                                             v.OBJECT_NAME),
                               status=204)
        HTTPretty.register_uri(HTTPretty.GET,
                               '%s/%s/%s' % (v.STORAGE_URL,
                                             v.CONTAINER_NAME,
                                             v.OBJECT_NAME),
                               status=200)
        self.assertTrue(self.bkup.retrieve_backup_data(v.OBJECT_NAME,
                                                       v.OBJECT_NAME))

    @httprettified
    def test_retrieve_no_container(self):
        """ unit test retrieve a object no container """
        HTTPretty.register_uri(HTTPretty.HEAD,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               status=404)
        self.assertRaises(RuntimeError,
                          self.bkup.retrieve_backup_data,
                          v.OBJECT_NAME)

    @httprettified
    def test_retrieve_backup_nodata(self):
        """ unit test retrieve no object """
        HTTPretty.register_uri(HTTPretty.HEAD,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               status=204)
        HTTPretty.register_uri(HTTPretty.GET,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               status=200,
                               body=json.dumps(v.OBJECTS))
        HTTPretty.register_uri(HTTPretty.HEAD,
                               '%s/%s/%s' % (v.STORAGE_URL,
                                             v.CONTAINER_NAME,
                                             v.OBJECT_NAME),
                               status=404)
        self.assertRaises(RuntimeError,
                          self.bkup.retrieve_backup_data,
                          v.OBJECT_NAME)

    @httprettified
    def test_retrieve_fail_backup_data(self):
        """ unit test fail retrieve a object """
        HTTPretty.register_uri(HTTPretty.HEAD,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               status=204)
        HTTPretty.register_uri(HTTPretty.GET,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               status=200,
                               body=json.dumps(v.OBJECTS))
        HTTPretty.register_uri(HTTPretty.HEAD,
                               '%s/%s/%s' % (v.STORAGE_URL,
                                             v.CONTAINER_NAME,
                                             v.OBJECT_NAME),
                               status=204)
        HTTPretty.register_uri(HTTPretty.GET,
                               '%s/%s/%s' % (v.STORAGE_URL,
                                             v.CONTAINER_NAME,
                                             v.OBJECT_NAME),
                               status=400)
        self.assertRaises(RuntimeError,
                          self.bkup.retrieve_backup_data,
                          v.OBJECT_NAME)

    @httprettified
    def test_retrieve_multiple_backup(self):
        """ unit test retrieve multiple objects """
        HTTPretty.register_uri(HTTPretty.HEAD,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               status=204)
        HTTPretty.register_uri(HTTPretty.GET,
                               '%s/%s' % (v.STORAGE_URL, v.CONTAINER_NAME),
                               status=200,
                               body=json.dumps(v.OBJECTS))
        for i in v.OBJECTS_NAME:
            HTTPretty.register_uri(HTTPretty.HEAD,
                                   '%s/%s/%s' % (v.STORAGE_URL,
                                                 v.CONTAINER_NAME,
                                                 i),
                                   status=204)
            HTTPretty.register_uri(HTTPretty.GET,
                                   '%s/%s/%s' % (v.STORAGE_URL,
                                                 v.CONTAINER_NAME,
                                                 i),
                                   status=200)
        self.assertTrue(self.bkup.delete_backup_data, v.OBJECTS_NAME)

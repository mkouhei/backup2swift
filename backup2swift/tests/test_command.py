# -*- coding: utf-8 -*-
""" backup2swift.tests.test_command """
import unittest
import os
import argparse
import sys
from backup2swift import __version__
from backup2swift import command as c
from backup2swift.tests import test_vars as v
if sys.version_info < (3, 0):
    from StringIO import StringIO
else:
    from io import StringIO


class CommandTests(unittest.TestCase):
    """ Test module for command. """

    def setUp(self):
        """ initialize """
        self.parser = argparse.ArgumentParser()
        self.capture = sys.stdout
        self.capture_err = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()

    def tearDown(self):
        """ finalize """
        sys.stdout = self.capture
        sys.stderr = self.capture_err
        if os.path.isfile('dummy'):
            os.remove('dummy')

    def test_check_config_file(self):
        """ unit test for check_config_file """
        self.assertEqual(v.CONFIG_FILE,
                         c.check_config_file(v.CONFIG_FILE))

    def test_check_config_file_fail(self):
        """ unit test for check_config_file fail case """
        if not os.path.isfile(os.path.join(os.path.expanduser('~'),
                                           '.bu2sw.conf')):
            self.assertRaises(IOError, c.check_config_file, None)

    def test_parse_options(self):
        """ unit test for parse_options """
        with self.assertRaises(SystemExit) as error:
            c.parse_options()
        self.assertEqual(2, error.exception.code)
        self.assertTrue(sys.stderr.getvalue())

    def test_setoption_version(self):
        """ unit test for version at set_option """
        c.setoption(self.parser, 'version')
        with self.assertRaises(SystemExit) as error:
            self.parser.parse_args('-V'.split())
        self.assertEqual(0, error.exception.code)
        if sys.version_info > (3, 4):
            self.assertEqual(__version__ + '\n', sys.stdout.getvalue())
        else:
            self.assertEqual(__version__ + '\n', sys.stderr.getvalue())

    def test_setoption_config(self):
        """ unit test for config at set_option """
        c.setoption(self.parser, 'config')
        self.assertEqual(
            self.parser.parse_args('-c dummy.conf'.split()).config,
            'dummy.conf')
        self.assertEqual(
            self.parser.parse_args('--config dummy.conf'.split()).config,
            'dummy.conf')

    def test_setoption_list_command(self):
        """ unit test for list command at set_option """
        c.setoption(self.parser, 'command')
        self.assertTrue(self.parser.parse_args('-l'.split()).list)
        self.assertTrue(self.parser.parse_args('--list'.split()).list)

    def test_setoption_push_command(self):
        """ unit test for push command at set_option """
        c.setoption(self.parser, 'command')
        self.assertEqual(['foo'],
                         self.parser.parse_args('-p foo'.split()).path)
        self.assertEqual(['foo', 'bar'],
                         self.parser.parse_args(
                             '--path foo bar'.split()).path)

    def test_setoption_stdin_command(self):
        """ unit test for stdin command at set_option """
        c.setoption(self.parser, 'command')
        self.assertEqual('foo',
                         self.parser.parse_args('-s foo'.split()).stdin)
        self.assertEqual('foo',
                         self.parser.parse_args('--stdin foo'.split()).stdin)

    def test_setoption_delete_command(self):
        """ unit test for delete command at set_option """
        c.setoption(self.parser, 'command')
        self.assertEqual(['foo'],
                         self.parser.parse_args('-d foo'.split()).delete)
        self.assertEqual(['foo', 'bar'],
                         self.parser.parse_args(
                             '--delete foo bar'.split()).delete)

    def test_setoption_retrieve_command(self):
        """ unit test for retrieve command at set_option """
        c.setoption(self.parser, 'command')
        self.assertEqual(['foo'],
                         self.parser.parse_args(
                             '-r foo'.split()).retrieve)
        self.assertEqual(['foo', 'bar'],
                         self.parser.parse_args(
                             '--retrieve foo bar'.split()).retrieve)

    def test_setoption_list_container(self):
        """ unit test for list command at set_option """
        c.setoption(self.parser, 'command')
        self.assertEqual('dummy',
                         self.parser.parse_args(
                             '-C dummy -l'.split()).container)
        self.assertEqual('dummy',
                         self.parser.parse_args(
                             '--container dummy -l'.split()).container)

    def test_setoption_list_verbose(self):
        """ unit test for list verbose command at set_option """
        c.setoption(self.parser, 'command')
        c.setoption(self.parser, 'verbose')
        self.assertTrue(self.parser.parse_args('-l -v'.split()).verbose)
        self.assertTrue(self.parser.parse_args('--list -v'.split()).verbose)
        self.assertTrue(self.parser.parse_args('-l --verbose'.split()).verbose)
        self.assertTrue(self.parser.parse_args(
            '--list --verbose'.split()).verbose)

    def test_setoption_retrieve_output(self):
        """ unit test for retrieve output command at set_option """
        c.setoption(self.parser, 'command')
        c.setoption(self.parser, 'verbose')
        self.assertEqual('bar',
                         self.parser.parse_args(
                             '-r foo -o bar'.split()).output)
        self.assertEqual('bar',
                         self.parser.parse_args(
                             '--r foo --output bar'.split()).output)

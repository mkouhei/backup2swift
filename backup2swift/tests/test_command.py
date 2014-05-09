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
import os
import argparse
import sys
if sys.version_info < (3, 0):
    from StringIO import StringIO
else:
    from io import StringIO
from backup2swift import __version__
from backup2swift import command as c
from backup2swift.tests import test_vars as v


class CommandTests(unittest.TestCase):

    def setUp(self):
        self.parser = argparse.ArgumentParser()
        self.capture = sys.stdout
        self.capture_err = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()

    def tearDown(self):
        sys.stdout = self.capture
        sys.stderr = self.capture_err

    def test_check_config_file(self):
        self.assertEqual(v.config_file,
                         c.check_config_file(v.config_file))

    def test_check_config_file_fail(self):
        if not os.path.isfile(os.path.join(os.environ['HOME'], '.bu2sw.conf')):
            self.assertRaises(IOError, c.check_config_file, None)

    def test_parse_options(self):
        with self.assertRaises(SystemExit) as e:
            c.parse_options()
        self.assertEqual(2, e.exception.code)
        self.assertTrue(sys.stderr.getvalue())

    def test_setoption_version(self):
        c.setoption(self.parser, 'version')
        with self.assertRaises(SystemExit) as e:
            self.parser.parse_args('-V'.split())
        self.assertEqual(0, e.exception.code)
        if sys.version_info > (3, 4):
            self.assertEqual(__version__ + '\n', sys.stdout.getvalue())
        else:
            self.assertEqual(__version__ + '\n', sys.stderr.getvalue())

    def test_setoption_config(self):
        c.setoption(self.parser, 'config')
        self.assertEqual(
            self.parser.parse_args('-c dummy.conf'.split()).config,
            'dummy.conf')
        self.assertEqual(
            self.parser.parse_args('--config dummy.conf'.split()).config,
            'dummy.conf')

    def test_setoption_list_command(self):
        c.setoption(self.parser, 'command')
        self.assertTrue(self.parser.parse_args('-l'.split()).list)
        self.assertTrue(self.parser.parse_args('--list'.split()).list)

    def test_setoption_push_command(self):
        c.setoption(self.parser, 'command')
        self.assertEqual(['foo'],
                         self.parser.parse_args('-p foo'.split()).path)
        self.assertEqual(['foo', 'bar'],
                         self.parser.parse_args(
                             '--path foo bar'.split()).path)

    def test_setoption_stdin_command(self):
        c.setoption(self.parser, 'command')
        self.assertEqual('foo',
                         self.parser.parse_args('-s foo'.split()).stdin)
        self.assertEqual('foo',
                         self.parser.parse_args('--stdin foo'.split()).stdin)

    def test_setoption_delete_command(self):
        c.setoption(self.parser, 'command')
        self.assertEqual(['foo'],
                         self.parser.parse_args('-d foo'.split()).delete)
        self.assertEqual(['foo', 'bar'],
                         self.parser.parse_args(
                             '--delete foo bar'.split()).delete)

    def test_setoption_retrieve_command(self):
        c.setoption(self.parser, 'command')
        self.assertEqual(['foo'],
                         self.parser.parse_args(
                             '-r foo'.split()).retrieve)
        self.assertEqual(['foo', 'bar'],
                         self.parser.parse_args(
                             '--retrieve foo bar'.split()).retrieve)

    def test_setoption_list_container(self):
        c.setoption(self.parser, 'command')
        self.assertEqual('dummy',
                         self.parser.parse_args(
                             '-C dummy -l'.split()).container)
        self.assertEqual('dummy',
                         self.parser.parse_args(
                             '--container dummy -l'.split()).container)

    def test_setoption_list_verbose(self):
        c.setoption(self.parser, 'command')
        c.setoption(self.parser, 'verbose')
        self.assertTrue(self.parser.parse_args('-l -v'.split()).verbose)
        self.assertTrue(self.parser.parse_args('--list -v'.split()).verbose)
        self.assertTrue(self.parser.parse_args('-l --verbose'.split()).verbose)
        self.assertTrue(self.parser.parse_args(
            '--list --verbose'.split()).verbose)

    def test_setoption_retrieve_output(self):
        c.setoption(self.parser, 'command')
        c.setoption(self.parser, 'verbose')
        self.assertEqual('bar',
                         self.parser.parse_args(
                             '-r foo -o bar'.split()).output)
        self.assertEqual('bar',
                         self.parser.parse_args(
                             '--r foo --output bar'.split()).output)

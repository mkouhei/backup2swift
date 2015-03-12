# -*- coding: utf-8 -*-
""" backup2swift.tests.test_config """
import unittest
from backup2swift import config as c


class ConfigTests(unittest.TestCase):
    """ test module config. """

    def test_check_config(self):
        """ unit test for check_config """
        self.assertEqual(('https://example.org/auth/v1.0',
                          'username',
                          'password',
                          10,
                          True,
                          5.0,
                          None),
                         c.check_config('examples/bu2sw.conf'))

    def test_check_config_ignore(self):
        """ unit test for check_config ignore case """
        self.assertEqual(('https://example.org/auth/v1.0',
                          'username',
                          'password',
                          10,
                          False,
                          5.0,
                          None),
                         c.check_config('examples/bu2sw_ignore_verify.conf'))

    def test_check_config_timeout(self):
        """ unit test for check_config ignore case """
        self.assertEqual(('https://example.org/auth/v1.0',
                          'username',
                          'password',
                          10,
                          True,
                          10.0,
                          None),
                         c.check_config('examples/bu2sw_timeout.conf'))

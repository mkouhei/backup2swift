# -*- coding: utf-8 -*-
""" backup2swift.tests """
import unittest
import backup2swift as b


class InitTests(unittest.TestCase):
    """ unit test for __init__ """

    def test__version__(self):
        """ check __version__ """
        self.assertTrue(b.__version__)

    def test__name__(self):
        """ check __name__ """
        self.assertTrue(b.__name__)

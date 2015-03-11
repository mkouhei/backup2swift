# -*- coding: utf-8 -*-
""" sample data for unit test """
import os.path

AUTH_URL = 'https://example.org/auth/v1.0'
STORAGE_URL = 'https://example.org/v1/username'
USERNAME = 'username'
PASSWORD = 'password'
TOKEN = 'hoge'
CONTAINER_NAME = 'fuga'
OBJECTS = [{'bytes': 5246,
            'content_type': 'text/plain',
            'hash': 'd226a3f396cbe3c187f2b7b78030eebb',
            'last_modified': '2013-05-01T08:40:00.459930',
            'name': 'sample.txt'},
           {'bytes': 5246,
            'content_type': 'text/plain',
            'hash': 'd226a3f396cbe3c187f2b7b78030eebb',
            'last_modified': '2013-05-01T09:23:40.060560',
            'name': 'sample2.txt'},
           {'bytes': 5246,
            'content_type': 'text/plain',
            'hash': 'd226a3f396cbe3c187f2b7b78030eebb',
            'last_modified': '2013-05-01T09:23:26.092580',
            'name': 'sample3.txt'}]
OBJECTS_NAME_L = [i.get('name') for i in OBJECTS]
TEST_FILE = os.path.abspath('backup2swift/tests/data/sample.txt')
TEST_FILES = [os.path.abspath('backup2swift/tests/data/sample.txt'),
              os.path.abspath('backup2swift/tests/data/sample2.txt')]
OBJECT_NAME = 'sample.txt'
OBJECTS_NAME = ['sample.txt', 'sample2.txt']
OBJECTS_HEADER = ['bytes', 'content_type', 'hash', 'last_modified', 'name']
HEADER_WIDTH = [5, 12, 4, 13, 4]
OBJECTS_ROW_WIDTH = [5, 12, 32, 26, 11]
DUMMY_ROW_WIDTH = [5, 12, 32, 26, 12]
CONFIG_FILE = 'examples/bu2sw.conf'

OBJECT_TABLE = ('------------------------------------------------------------'
                '-------------------------------\nname        last_modified  '
                '            hash                             content_type byt'
                'es  \n------------------------------------------------------'
                '-------------------------------------\nsample.txt  2013-05-0'
                '1T08:40:00.459930 d226a3f396cbe3c187f2b7b78030eebb text/plain'
                '   5246   \nsample2.txt 2013-05-01T09:23:40.060560 d226a3f39'
                '6cbe3c187f2b7b78030eebb text/plain   5246   \nsample3.txt 20'
                '13-05-01T09:23:26.092580 d226a3f396cbe3c187f2b7b78030eebb tex'
                't/plain   5246   \n-----------------------------------------'
                '--------------------------------------------------\n')

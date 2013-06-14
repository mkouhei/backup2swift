# -*- coding: utf-8 -*-
import os.path

auth_url = 'https://example.org/auth/v1.0'
username = 'username'
password = 'password'
token = 'hoge'
s_url = 'fuga'
container_name = 'moge'
objects = [{'bytes': 5246,
            'content_type': 'text/plain',
            'hash': 'd226a3f396cbe3c187f2b7b78030eebb',
            'last_modified': '2013-05-01T08:40:00.459930',
            'name': 'sample.txt'},
           {'bytes': 5246,
            'content_type': 'text/plain',
            'hash': 'd226a3f396cbe3c187f2b7b78030eebb',
            'last_modified': '2013-05-01T09:23:40.060560',
            'name': 'sample_2.txt'},
           {'bytes': 5246,
            'content_type': 'text/plain',
            'hash': 'd226a3f396cbe3c187f2b7b78030eebb',
            'last_modified': '2013-05-01T09:23:26.092580',
            'name': 'sample_3.txt'}]
objects_name_l = [i.get('name') for i in objects]
test_file = os.path.abspath('src/backup2swift_tests/sample.txt')
test_files = [os.path.abspath('src/backup2swift_tests/sample.txt'),
              os.path.abspath('src/backup2swift_tests/sample2.txt')]
object_name = 'sample.txt'
objects_name = ['sample.txt', 'sample2.txt']
objects_header = ['bytes', 'content_type', 'hash', 'last_modified', 'name']
header_width = [5, 12, 4, 13, 4]
objects_row_width = [5, 12, 32, 26, 12]
dummy_row_width = [5, 12, 32, 26, 11]
config_file = 'examples/bu2sw.conf'

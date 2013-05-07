# -*- coding: utf-8 -*-
import os.path
auth_url = 'https://example.org/auth/v1.0'
username = 'username'
password = 'password'
token = 'hoge'
s_url = 'fuga'
container_name = 'moge'
objects = [{u'bytes': 5246,
            u'content_type': u'text/plain',
            u'hash': u'd226a3f396cbe3c187f2b7b78030eebb',
            u'last_modified': u'2013-05-01T08:40:00.459930',
            u'name': u'sample.txt'},
           {u'bytes': 5246,
            u'content_type': u'text/plain',
            u'hash': u'd226a3f396cbe3c187f2b7b78030eebb',
            u'last_modified': u'2013-05-01T09:23:40.060560',
            u'name': u'sample_2.txt'},
           {u'bytes': 5246,
            u'content_type': u'text/plain',
            u'hash': u'd226a3f396cbe3c187f2b7b78030eebb',
            u'last_modified': u'2013-05-01T09:23:26.092580',
            u'name': u'sample_3.txt'}]
objects_name_l = [i.get('name') for i in objects]
test_file = os.path.abspath('src/backup2swift_tests/sample.txt')
object_name = 'sample.txt'

# -*- coding: utf-8 -*-
"""
    Copyright (C) 2013 Kouhei Maeda <mkouhei@palmtb.net>

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
from swiftsc import client
import socket
import os.path
import glob
from datetime import datetime


ROTATE_LIMIT = 10
FQDN = socket.getfqdn()


class Backup(object):
    def __init__(self, auth_url, username, password, container_name=FQDN):
        self.token, self.storage_url = client.retrieve_token(auth_url,
                                                             username,
                                                             password)
        self.container_name = container_name

    def backup(self, target_path):
        if os.path.isdir(target_path):
            [self.backup_file(f) for f in glob.glob(target_path + '/*')]
        elif os.path.isfile(target_path):
            self.backup_file(target_path)

    def backup_file(self, filename):
        object_name = os.path.basename(filename)

        if client.is_container(self.token, self.storage_url,
                               self.container_name) == 204:
            # 204; No Content
            rc = client.create_container(self.token,
                                         self.storage_url,
                                         self.container_name)
            if not (rc == 201 or rc == 202):
                # 201; Created, 202; Accepted
                raise RuntimeError('failed to create the container "%s".'
                                   % self.container_name)

        objects_list = [object.get('name') for object in
                        client.list_objects(self.token,
                                            self.storage_url,
                                            self.container_name)]
        print objects_list
        print object_name

        if object_name in objects_list:
            self.rotate(filename, object_name, objects_list)
        else:
            rc = client.create_object(self.token,
                                      self.storage_url,
                                      self.container_name,
                                      filename)
            if not (rc == 201 or rc == 202):
                raise RuntimeError('failed to create the object "%s".'
                                   % object_name)

    def rotate(self, filename, object_name, objects_list,
               rotate_limit=ROTATE_LIMIT):

        # copy current object to new object
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        new_object_name = object_name + '_' + timestamp
        rc = client.copy_object(self.token, self.storage_url,
                                self.container_name,
                                object_name, new_object_name)
        if rc != 201:
            raise RuntimeError('failed to copy object "%s".' % new_object_name)

        # create new object
        rc = client.create_object(self.token, self.storage_url,
                                  self.container_name, filename)
        if rc != 201:
            raise RuntimeError('failed to create the object "%s".'
                               % object_name)

        # delete old objects
        archive_list = [obj for obj in objects_list
                        if obj.startswith(object_name + '_')]
        archive_list.reverse()
        [client.delete_object(self.token, self.storage_url,
                              self.container_name, obj)
         for i, obj in enumerate(archive_list) if i + 1 > rotate_limit - 1]

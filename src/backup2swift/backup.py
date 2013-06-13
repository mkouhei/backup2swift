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
import os.path
import glob
import sys
from datetime import datetime
from swiftsc import client
from backup2swift import utils

ROTATE_LIMIT = 10


class Backup(object):
    def __init__(self, auth_url, username, password, rotate_limit=ROTATE_LIMIT,
                 verify=True, tenant_id=None, container_name=utils.FQDN):
        self.verify = verify
        (self.token,
         self.storage_url) = client.retrieve_token(auth_url,
                                                   username,
                                                   password,
                                                   tenant_id,
                                                   verify=self.verify)
        if isinstance(rotate_limit, str):
            self.rotate_limit = int(rotate_limit)
        else:
            self.rotate_limit = rotate_limit
        self.container_name = container_name

    def backup(self, target_path):
        """

        Argument:
            target_path: path of backup target file or directory
        """
        if isinstance(target_path, list):
            # for multiple arguments
            [utils.multiprocess(self.backup, path) for path in target_path]
        elif os.path.isdir(target_path):
            [utils.multiprocess(self.backup_file, f)
             for f in glob.glob(os.path.join(target_path, '*'))]
        elif os.path.isfile(target_path):
            self.backup_file(target_path)
        return True

    def backup_file(self, filename):
        """

        Argument:
            filename: path of backup target file
        """
        object_name = os.path.basename(filename)

        if not client.is_container(self.token, self.storage_url,
                                   self.container_name, verify=self.verify):
            # False is no container
            rc = client.create_container(self.token,
                                         self.storage_url,
                                         self.container_name,
                                         verify=self.verify)
            if not (rc == 201 or rc == 202):
                # 201; Created, 202; Accepted
                raise RuntimeError('Failed to create the container "%s"'
                                   % self.container_name, verify=self.verify)

        objects_list = [object.get('name') for object in
                        client.list_objects(self.token,
                                            self.storage_url,
                                            self.container_name,
                                            verify=self.verify)]

        if object_name in objects_list:
            self.rotate(filename, object_name, objects_list)
        else:
            rc = client.create_object(self.token,
                                      self.storage_url,
                                      self.container_name,
                                      filename,
                                      verify=self.verify)
            if not (rc == 201 or rc == 202):
                raise RuntimeError('Failed to create the object "%s"'
                                   % object_name)
        return True

    def rotate(self, filename, object_name, objects_list):
        """

        Arguments:
            filename:     filename of backup target
            object_name:  name of object on Swift
            objects_list: list of objects on Swift
        """
        # copy current object to new object
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        new_object_name = object_name + '_' + timestamp
        rc = client.copy_object(self.token, self.storage_url,
                                self.container_name, object_name,
                                new_object_name, verify=self.verify)
        if rc != 201:
            raise RuntimeError('Failed to copy object "%s"' % new_object_name)

        # create new object
        rc = client.create_object(self.token, self.storage_url,
                                  self.container_name, filename,
                                  verify=self.verify)
        if rc != 201:
            raise RuntimeError('Failed to create the object "%s"'
                               % object_name)

        # delete old objects
        archive_list = [obj for obj in objects_list
                        if obj.startswith(object_name + '_')]
        archive_list.reverse()
        [utils.multiprocess(client.delete_object, self.token,
                            self.storage_url, self.container_name,
                            obj, verify=self.verify)
         for i, obj in enumerate(archive_list)
         if i + 1 > self.rotate_limit - 1]
        return True

    def retrieve_backup_data_list(self, verbose=False):
        """

        Argument:
            verbose: boolean flag of listing objects
        """
        if not client.is_container(self.token, self.storage_url,
                                   self.container_name, verify=self.verify):
            return []

        if verbose:
            backup_l = [i for i in client.list_objects(self.token,
                                                       self.storage_url,
                                                       self.container_name,
                                                       verify=self.verify)]
        else:
            backup_l = [i.get('name') for i
                        in client.list_objects(self.token,
                                               self.storage_url,
                                               self.container_name,
                                               verify=self.verify)]
        return backup_l

    def retrieve_backup_data(self, object_name, output_filepath=None):
        """

        Argument:
            object_name: delete target object name
        """
        if isinstance(object_name, list):
            # for retrieve multiple objects
            output_filepath = None
            [utils.multiprocess(self.retrieve_backup_data, obj)
             for obj in object_name]
        elif (client.is_container(self.token, self.storage_url,
                                  self.container_name, verify=self.verify) and
              client.is_object(self.token, self.storage_url,
                               self.container_name, object_name,
                               verify=self.verify)):
            rc, content = client.retrieve_object(self.token,
                                                 self.storage_url,
                                                 self.container_name,
                                                 object_name,
                                                 verify=self.verify)
            if not rc:
                raise RuntimeError('Failed to retrieve the object "%s"'
                                   % object_name)
            if output_filepath:
                fpath = os.path.abspath(output_filepath)
                dpath = os.path.dirname(fpath)
                if not os.path.isdir(dpath):
                    raise IOError('No such directory "%s"' % dpath)
            else:
                dpath = os.path.abspath(os.curdir)
                fpath = os.path.join(dpath, object_name)
            if sys.version_info > (3, 0) and isinstance(content, bytes):
                mode = 'bw'
            else:
                mode = 'w'
            with open(fpath, mode) as f:
                f.write(content)
        else:
            raise RuntimeError('No such object "%s"' % object_name)

    def delete_backup_data(self, object_name):
        """

        Argument:
            object_name: delete target object name
        """
        if isinstance(object_name, list):
            # for multiple arguments
            [self.delete_backup_data(obj) for obj in object_name]

        elif (client.is_container(self.token, self.storage_url,
                                  self.container_name, verify=self.verify) and
              client.is_object(self.token, self.storage_url,
                               self.container_name, object_name,
                               verify=self.verify)):
            rc = client.delete_object(self.token,
                                      self.storage_url,
                                      self.container_name,
                                      object_name,
                                      verify=self.verify)
            if not rc == 204:
                raise RuntimeError('Failed to delete the object "%s"'
                                   % object_name)
            return True
        else:
            raise RuntimeError('No such object "%s"' % object_name)

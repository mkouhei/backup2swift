# -*- coding: utf-8 -*-
"""backup2swift.backup module."""
import os.path
import glob
import sys
from datetime import datetime
from swiftsc import Client
from backup2swift import utils

ROTATE_LIMIT = 10


class Backup(object):
    """Backup class.

    Arguments:
        auth_url:       authentication url of swift
        username:       username for swift
        password:       password for swift
        rotate_limit:   limitation count of rotation
        verify:         verification of ssl certification
        tenant_id:      tenant id when using KeyStone
        container_name: container name of swift
    """

    def __init__(self, *args, **kwargs):
        """Initialize Backup object."""
        self.client = Client(auth_uri=args[0],
                             username=args[1],
                             password=args[2],
                             tenant_name=kwargs.get('tenant_id'),
                             verify=kwargs.get('verify'),
                             timeout=kwargs.get('timeout'))

        if kwargs.get('rotate_limit'):
            self.rotate_limit = kwargs.get('rotate_limit')
        else:
            self.rotate_limit = ROTATE_LIMIT

        if kwargs.get('container_name'):
            self.container_name = kwargs.get('container_name')
        else:
            self.container_name = utils.FQDN
        self.client.containers.container(self.container_name)

    def backup(self, target_path):
        """Base Backup method.

        Argument:
            target_path: path of backup target file or directory
        """
        if isinstance(target_path, list):
            # for multiple arguments
            [utils.multiprocess(self.backup, path) for path in target_path]
        elif os.path.isdir(target_path):
            [utils.multiprocess(self.backup_file, f)
             for f in glob.glob(os.path.join(target_path, '*'))]
            return True
        elif os.path.isfile(target_path):
            self.backup_file(target_path)
            return True
        else:
            return False

    def backup_file(self, filename, data=None):
        """Backup file.

        Argument:
            filename: path of backup target file
            data:     backup target file content from stdin pipe
        """
        object_name = os.path.basename(filename)
        if not self.client.containers.show_metadata(self.container_name).ok:
            # False is no container
            res = self.client.containers.create(name=self.container_name)
            if not (res.status_code == 201 or res.status_code == 202):
                # 201; Created, 202; Accepted
                raise RuntimeError('Failed to create the container "%s"'
                                   % self.container_name)

        objects_list = [obj.get('name') for obj in
                        self.client.containers.objects.list().json()]

        if filename and data:
            # from stdin pipe
            object_name = filename
            filename = data

        if object_name in objects_list:
            self.rotate(filename, object_name, objects_list)
        else:
            res = self.client.containers.objects.create(name=object_name,
                                                        file_path=filename)
            if not (res.status_code == 201 or res.status_code == 202):
                raise RuntimeError('Failed to create the object "%s"'
                                   % object_name)
        return True

    def rotate(self, filename, object_name, objects_list):
        """Rotate data.

        Arguments:
            filename:     filename of backup target
            object_name:  name of object on Swift
            objects_list: list of objects on Swift
        """
        # copy current object to new object
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        new_object_name = object_name + '_' + timestamp

        res = self.client.containers.objects.copy(object_name,
                                                  new_object_name)
        if res.status_code != 201:
            raise RuntimeError('Failed to copy object "%s"' % new_object_name)

        # create new object
        res = self.client.containers.objects.create(name=object_name,
                                                    file_path=filename)
        if res.status_code != 201:
            raise RuntimeError('Failed to create the object "%s"'
                               % object_name)

        # delete old objects
        archive_list = [obj for obj in objects_list
                        if obj.startswith(object_name + '_')]
        archive_list.reverse()

        [utils.multiprocess(self.client.containers.objects.delete, obj)
         for i, obj in enumerate(archive_list)
         if i + 1 > self.rotate_limit - 1]
        return True

    def retrieve_backup_data_list(self, verbose=False):
        """Retrieve the list of backup data.

        Argument:
            verbose: boolean flag of listing objects
        """
        if not self.client.containers.show_metadata(self.container_name).ok:
            return []

        if verbose:
            objects = [i for i in self.client.containers.objects.list().json()]
        else:
            objects = [i.get('name') for i
                       in self.client.containers.objects.list().json()]
        return objects

    def retrieve_backup_data(self, object_name, output_filepath=None):
        """Retrieve backup data.

        Argument:
            object_name: delete target object name
        """
        if isinstance(object_name, list):
            # for retrieve multiple objects
            output_filepath = None
            [utils.multiprocess(self.retrieve_backup_data, obj)
             for obj in object_name]
        elif (self.client.containers.show_metadata(self.container_name).ok and
              self.client.containers.objects.show_metadata(object_name).ok):
            res = self.client.containers.objects.detail(object_name)

            if not res.ok:
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
            if sys.version_info > (3, 0) and isinstance(res.content, bytes):
                mode = 'bw'
            else:
                mode = 'w'
            with open(fpath, mode) as _file:
                _file.write(res.content)
                return True
        else:
            raise RuntimeError('No such object "%s"' % object_name)

    def delete_backup_data(self, object_name):
        """Delete backup data.

        Argument:
            object_name: delete target object name
        """
        if isinstance(object_name, list):
            # for multiple arguments
            [self.delete_backup_data(obj) for obj in object_name]
        elif (self.client.containers.show_metadata(self.container_name).ok and
              self.client.containers.objects.show_metadata(object_name).ok):
            res = self.client.containers.objects.delete(object_name)
            if not res.status_code == 204:
                raise RuntimeError('Failed to delete the object "%s"'
                                   % object_name)
            return True
        else:
            raise RuntimeError('No such object "%s"' % object_name)

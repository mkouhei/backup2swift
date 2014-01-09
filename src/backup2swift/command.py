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
import argparse
import os
import os.path
import sys
from backup2swift import __version__, backup, utils, config

DEFAULT_CONF = '.bu2sw.conf'


def parse_options():
    parser = argparse.ArgumentParser(description='usage')
    setoption(parser, 'version')
    setoption(parser, 'config')
    setoption(parser, 'command')
    setoption(parser, 'verbose')
    args = parser.parse_args()
    return args


def setoption(parser, keyword):
    """

    Arguments:
        parser: object of argparse
        keyword: switching keyword
    """
    if keyword == 'version':
        parser.add_argument('-V', '--version', action='version',
                            version=__version__)
    elif keyword == 'config':
        parser.add_argument('-c', '--config', action='store',
                            help='configuraton file of backup2swift')
    elif keyword == 'verbose':
        parser.add_argument('-v', '--verbose', action='store_true',
                            help='list verbose')
        parser.add_argument('-o', '--output', action='store',
                            help=('specify filename of retrieved data'
                                  ' (only retrieving simple object)'))
    elif keyword == 'command':
        parser.add_argument('-C', '--container', action='store',
                            help=('specify container name (default: '
                                  'FQDN of host when executes this command)'))
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-l', '--list', action='store_true',
                           help='listing object data')
        group.add_argument('-p', '--path', action='store', nargs='+',
                           help='target files/dir path of backup')
        group.add_argument('-s', '--stdin', action='store',
                           help='backup fromstdin pipe & specify object name')
        group.add_argument('-d', '--delete', action='store', nargs='+',
                           help='delete backup data')
        group.add_argument('-r', '--retrieve', action='store', nargs='+',
                           help='retrieve backup data')
        parser.set_defaults(func=execute_swift_client)


def check_config_file(args_config):
    """

    Argument:
        args_config: args.config
    """
    if args_config:
        # override configuration file path
        config_file = args_config
    elif os.path.isfile(os.path.join(os.environ['HOME'], DEFAULT_CONF)):
        # use default configuration file
        config_file = os.path.join(os.environ['HOME'], DEFAULT_CONF)
    else:
        raise IOError(('Setup "~/.bu2sw.conf" or '
                       'specify configuration file with "-c" option'))
    return config_file


def execute_swift_client(args):
    """

    Argument:
        args: argument object
    """
    config_file = check_config_file(args.config)
    (auth_url, username, password, rotate_limit,
     verify, tenant_id) = config.check_config(config_file)
    if args.container:
        container_name = args.container
    else:
        container_name = utils.FQDN
    b = backup.Backup(auth_url, username, password, rotate_limit,
                      verify=verify, tenant_id=tenant_id,
                      container_name=container_name)
    if args.list:
        # listing backup data
        backup_l = b.retrieve_backup_data_list(args.verbose)
        utils.list_data(backup_l)
    elif args.path:
        # backup data to swift
        b.backup(args.path)
    elif args.stdin:
        # backup via stdin pipe
        if sys.version_info > (3, 0):
            # for python3
            b.backup_file(args.stdin, data=sys.stdin.buffer.raw)
        else:
            # for python2
            b.backup_file(args.stdin, data=sys.stdin)
    elif args.retrieve:
        # retrive backup data
        b.retrieve_backup_data(args.retrieve, args.output)
    elif args.delete:
        # delete backup data
        b.delete_backup_data(args.delete)


def main():
    try:
        args = parse_options()
        args.func(args)
    except (RuntimeError, IOError) as error:
        # syslog.ERR is 3
        utils.logging(3, error)

if __name__ == '__main__':
    main()

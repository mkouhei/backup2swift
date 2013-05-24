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
import argparse
import config
from __init__ import __version__
import backup
import utils


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
                            required=True,
                            help='configuraton file of backup2swift')
    elif keyword == 'verbose':
        parser.add_argument('-v', '--verbose', action='store_true',
                            help='list verbose')
        parser.add_argument('-o', '--output', action='store',
                            help='specify filename of retrieved data')
    elif keyword == 'command':
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-l', '--list', action='store_true',
                           help='listing object data')
        group.add_argument('-p', '--path', action='store',
                           help='target file/dir path of backup')
        group.add_argument('-d', '--delete', action='store',
                           help='delete backup data')
        group.add_argument('-r', '--retrieve', action='store',
                           help='retrieve backup data')
        parser.set_defaults(func=execute_swift_client)


def execute_swift_client(args):
    """

    Argument:
        args: argument object
    """
    (auth_url, username, password,
     rotate_limit, verify) = config.check_config(args.config)
    b = backup.Backup(auth_url, username, password, verify=verify)
    if args.list:
        # listing backup data
        backup_l = b.retrieve_backup_data_list(args.verbose)
        utils.list_data(backup_l)
    elif args.path:
        # backup data to swift
        b.backup(args.path)
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
    except RuntimeError as error:
        # syslog.ERR is 3
        utils.logging(3, error)

if __name__ == '__main__':
    main()

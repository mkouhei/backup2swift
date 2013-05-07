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
    setoption(parser, 'target_filepath')
    args = parser.parse_args()
    return args


def setoption(parser, keyword):
    if keyword == 'version':
        parser.add_argument('-V', '--version', action='version',
                            version=__version__)
    elif keyword == 'config':
        parser.add_argument('-c', '--config', action='store',
                            required=True,
                            help='configuraton file of backup2swift')
    elif keyword == 'target_filepath':
                parser.add_argument('target_file', action='store',
                                    help='target file path of backup')
    parser.set_defaults(func=backup_to_swift)


def backup_to_swift(args):
    (auth_url, username,
     password, rotate_limit) = config.check_config(args.config)
    b = backup.Backup(auth_url, username, password)
    b.backup(args.target_file)


def main():
    try:
        args = parse_options()
        args.func(args)
    except RuntimeError as error:
        # syslog.ERR is 3
        utils.logging(3, error)

if __name__ == '__main__':
    main()

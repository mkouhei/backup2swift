# -*- coding: utf-8 -*-
"""backup2swift.command module."""
import argparse
import os
import os.path
import sys
from swiftsc.exception import AuthenticationError
from backup2swift import __version__, backup, utils, config

DEFAULT_CONF = '.bu2sw.conf'


def parse_options():
    """setup options."""
    parser = argparse.ArgumentParser(description='usage')
    setoption(parser, 'version')
    setoption(parser, 'config')
    setoption(parser, 'command')
    setoption(parser, 'verbose')
    args = parser.parse_args()
    return args


def setoption(parser, keyword):
    """Set option of argument parser.

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
    """Check configuration file.

    Argument:
        args_config: args.config
    """
    if args_config:
        # override configuration file path
        config_file = args_config
    elif os.path.isfile(os.path.join(os.path.expanduser('~'), DEFAULT_CONF)):
        # use default configuration file
        config_file = os.path.join(os.path.expanduser('~'), DEFAULT_CONF)
    else:
        raise IOError(('Setup "~/.bu2sw.conf" or '
                       'specify configuration file with "-c" option'))
    return config_file


def execute_swift_client(args):
    """Execute swift client.

    Argument:
        args: argument object
    """
    config_file = check_config_file(args.config)
    (auth_url, username, password, rotate_limit,
     verify, timeout, tenant_id) = config.check_config(config_file)
    if args.container:
        container_name = args.container
    else:
        container_name = utils.FQDN
    bkup = backup.Backup(auth_url, username, password,
                         rotate_limit=rotate_limit,
                         verify=verify,
                         timeout=timeout,
                         tenant_id=tenant_id,
                         container_name=container_name)
    if args.list:
        # listing backup data
        backup_l = bkup.retrieve_backup_data_list(args.verbose)
        utils.list_data(backup_l)
    elif args.path:
        # backup data to swift
        bkup.backup(args.path)
    elif args.stdin:
        # backup via stdin pipe
        if sys.version_info > (3, 0):
            # for python3
            bkup.backup_file(args.stdin, data=sys.stdin.buffer.raw)
        else:
            # for python2
            bkup.backup_file(args.stdin, data=sys.stdin)
    elif args.retrieve:
        # retrive backup data
        bkup.retrieve_backup_data(args.retrieve, args.output)
    elif args.delete:
        # delete backup data
        bkup.delete_backup_data(args.delete)


def main():
    """main function."""
    try:
        args = parse_options()
        args.func(args)
    except (RuntimeError, IOError, AuthenticationError) as error:
        # syslog.ERR is 3
        utils.logging(3, error)

if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
"""backup2swift.config module."""
import sys
from backup2swift import utils
if sys.version_info > (2, 6) and sys.version_info < (2, 8):
    import ConfigParser as configparser
elif sys.version_info > (3, 0):
    import configparser


#: connection timeout
#: see also http://goo.gl/6KIJnc
TIMEOUT = 5.000


def check_config(filename):
    """Check configuration file of backup2swift.

    Argument:

        filename: config file path (default is ~/.bu2sw.conf)
    """
    try:
        conf = configparser.SafeConfigParser(allow_no_value=False)
    except TypeError as error:
        msg = "__init__() got an unexpected keyword argument 'allow_no_value'"
        if str(error) == msg:
            # for argparse using python 2.6
            conf = configparser.SafeConfigParser()
        else:
            utils.logging(3, error)
    conf.read(filename)
    try:
        auth_url = conf.get('swift', 'auth_url')
        username = conf.get('swift', 'username')
        password = conf.get('swift', 'password')
        rotate_limit = int(conf.get('backup', 'rotate_limit'))
    except (configparser.NoSectionError, configparser.NoOptionError) as error:
        # syslog.ERR is 3
        utils.logging(3, error)
    try:
        if conf.get('swift', 'ignore_verify_ssl_certification') == 'True':
            verify = False
        else:
            verify = True
    except (configparser.NoSectionError, configparser.NoOptionError):
        verify = True

    try:
        timeout = float(conf.get('swift', 'timeout'))
    except (configparser.NoSectionError, configparser.NoOptionError):
        timeout = TIMEOUT

    try:
        if conf.get('keystone', 'tenant_id'):
            tenant_id = conf.get('keystone', 'tenant_id')
        else:
            tenant_id = None
    except (configparser.NoSectionError, configparser.NoOptionError):
        tenant_id = None

    return (auth_url, username, password, rotate_limit,
            verify, timeout, tenant_id)

# -*- coding: utf-8 -*-
"""
    Copyright (C) 2013-2015 Kouhei Maeda <mkouhei@palmtb.net>

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
import syslog
import multiprocessing
import socket
import backup2swift

FQDN = socket.getfqdn()


def logging(priority, message):
    """

    Arguments:
        priority: syslog priority
        message: log message
    """
    syslog.openlog(backup2swift.__name__, syslog.LOG_PID, syslog.LOG_LOCAL0)
    syslog.syslog(priority, str(message))
    syslog.closelog()
    print(message)
    exit(1)


def list_data(data):
    """

    Argument:
        data: list of data
    """
    for i in data:
        if isinstance(i, dict):
            pretty_print(list(i.keys()), data)
            break
        else:
            print(i)


def pretty_print(header, rows):
    """

    Arguments:
        header: list of header data
        rows:   list of data
    """
    # formatting header
    header.sort()
    header.reverse()
    # retrieve column width from header
    col_width_l = [len(i) for i in header]

    # retrieve column width from data
    col_width_l = get_columns_width(col_width_l, header, rows)

    # print formatly
    print_header(col_width_l, header)
    for row in rows:
        print(generate_row_s(row, col_width_l, header))
    print_footer(col_width_l)


def get_columns_width(columns_width, header, rows):
    """

    Arguments:
        columns_width: list of columns string length
        header:        list of header data
        rows:          list of data
    """
    for row in rows:
        for i, key in enumerate(header):
            value = str(row.get(key))
            if columns_width[i] <= len(value):
                columns_width[i] = len(value)
            else:
                columns_width[i] = columns_width[i]
    return columns_width


def print_header(columns_width, header):
    """

    Arguments:
        columns_width: list of columns string length
        header:        list of header data
    """
    border = ''
    for col_width in columns_width:
        border += "-" * col_width + '-'

    print("%s" % border)
    print(generate_row_s(header, columns_width))
    print("%s" % border)


def print_footer(columns_width):
    """

    Argument:
        columns_width: list of columns string length
    """
    border = ''
    for _, col_width in enumerate(columns_width):
        border += "-" * col_width + '-'
    print("%s" % border)


def generate_row_s(row, columns_width, header=None):
    """

    Arguments:
        row:           data of row
        columns_width: list of columns string length
        header:        list of header data
    """
    row_s = ''

    if header:
        for i, key in enumerate(header):
            column = str(row.get(key))
            row_s += (column + ' ' *
                      (columns_width[i] - len(column) + 1))
        row_s += ' '
    else:
        for i, value in enumerate(row):
            column = str(value)
            row_s += (column + ' ' *
                      (columns_width[i] - len(column) + 1))
        row_s += ' '
    return row_s


def multiprocess(func, *args, **kwargs):
    """ multiprocessing for backup / delete object / retrieve object. """
    proc = multiprocessing.Process(target=func, args=args, kwargs=kwargs)
    proc.start()

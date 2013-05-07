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
import syslog
import sys


def logging(priority, message):
    syslog.openlog('bu2sw', syslog.LOG_PID, syslog.LOG_LOCAL0)
    syslog.syslog(priority, str(message))
    syslog.closelog()
    print(message)
    exit(1)


def list_data(data):
    for i in data:
        if isinstance(i, unicode):
            print(i)
        elif isinstance(i, dict):
            pretty_print(i.keys(), data)
            break


def pretty_print(header, rows):
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
        print generate_row_s(row, col_width_l, header)
    print_footer(col_width_l)


def get_columns_width(columns_width, header, rows):
    for row in rows:
        for i, key in enumerate(header):
            value = str(row.get(key))
            if columns_width[i] <= len(value):
                columns_width[i] = len(value)
            else:
                columns_width[i] = columns_width[i]
    return columns_width


def print_header(cols_width, header):
    border = '+'
    for col_width in cols_width:
        border += "-" * (col_width + 1) + '-+'

    sys.stdout.write("%s\n" % border)
    print(generate_row_s(header, cols_width))
    sys.stdout.write("%s\n" % border)


def print_footer(cols_width):
    border = '+'
    for i, col_width in enumerate(cols_width):
        border += "-" * (col_width + 1) + '-+'
    sys.stdout.write("%s\n" % border)


def generate_row_s(row, columns_width, header=None):
    row_s = ''

    if header:
        for i, key in enumerate(header):
            column = str(row.get(key))
            row_s += ('| ' + column + ' ' *
                      (columns_width[i] - len(column) + 1))
        row_s += '|'
    else:
        for i, value in enumerate(row):
            column = str(value)
            row_s += ('| ' + column + ' ' *
                      (columns_width[i] - len(column) + 1))
        row_s += '|'
    return row_s

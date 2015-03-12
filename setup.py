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

import os.path
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import backup2swift


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', 'Arguments to pass to tox')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        import shlex
        if self.tox_args:
            errno = tox.cmdline(args=shlex.split(self.tox_args))
        else:
            errno = tox.cmdline(self.test_args)
        sys.exit(errno)


classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: "
    "GNU General Public License v3 or later (GPLv3+)",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Internet",
    "Topic :: Internet :: WWW/HTTP",
    "Environment :: OpenStack",
]

long_description = (
    open("README.rst").read() +
    open(os.path.join("docs", "TODO.rst")).read() +
    open(os.path.join("docs", "HISTORY.rst")).read())

requires = ['setuptools',
            'swiftsc>=0.6.2']

with open('requirements.txt', 'w') as fobj:
    fobj.write('\n'.join(requires))

setup(name='backup2swift',
      version=backup2swift.__version__,
      description='Backup data to OpenStack Swift',
      long_description=long_description,
      author='Kouhei Maeda',
      author_email='mkouhei@palmtb.net',
      url='https://github.com/mkouhei/backup2swift',
      license=' GNU General Public License version 3',
      classifiers=classifiers,
      packages=find_packages(),
      data_files=[('share/backup2swift/examples',
                   ['examples/bu2sw.conf',
                    'examples/bu2sw_ignore_verify.conf'])],
      install_requires=requires,
      tests_require=['tox'],
      cmdclass={'test': Tox},
      entry_points={
          "console_scripts": ["bu2sw = backup2swift.command:main"]
      },)

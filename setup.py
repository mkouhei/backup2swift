# -*- coding: utf-8 -*-
"""setup.py."""
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


def read_content(filepath):
    with open(filepath) as fobj:
        return fobj.read()


classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: "
    "GNU General Public License v3 or later (GPLv3+)",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Internet",
    "Topic :: Internet :: WWW/HTTP",
    "Environment :: OpenStack",
]

long_description = (
    read_content("README.rst") +
    read_content(os.path.join("docs", "TODO.rst")) +
    read_content(os.path.join("docs", "HISTORY.rst")))

requires = ['setuptools',
            'swiftsc>=0.7.2']
extras_require = {
    'reST': ['Sphinx']}

if os.environ.get('READTHEDOCS', None):
    extras_require['reST'].append('recommonmark')

setup(name='backup2swift',
      version=backup2swift.__version__,
      description='Backup data to OpenStack Swift',
      long_description=long_description,
      author='Kouhei Maeda',
      author_email='mkouhei@palmtb.net',
      url='https://github.com/mkouhei/backup2swift',
      license='GNU General Public License version 3',
      classifiers=classifiers,
      packages=find_packages(),
      data_files=[('share/backup2swift/examples',
                   ['examples/bu2sw.conf',
                    'examples/bu2sw_ignore_verify.conf'])],
      install_requires=requires,
      extras_require=extras_require,
      tests_require=['tox'],
      cmdclass={'test': Tox},
      entry_points={
          "console_scripts": ["bu2sw = backup2swift.command:main"]
      },)

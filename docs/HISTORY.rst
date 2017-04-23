History
-------

0.9.5 (2017-04-23)
^^^^^^^^^^^^^^^^^^

* Updates swiftsc version.
* Supports Python 3.6.

0.9.4 (2015-09-05)
^^^^^^^^^^^^^^^^^^

* Adds handling of authentiction error.

0.9.3 (2015-08-31)
^^^^^^^^^^^^^^^^^^

* Change dependency swiftsc version (Supports Identity API v3).
* Supports Python 3.5 (3.5.0-rc2).
* Fixes requests-mock package name.

0.9.2 (2015-05-17)
^^^^^^^^^^^^^^^^^^

* Changes os.environ['HOME'] to os.expanduser('~').
* Changes httpretty to requests_mock.
* Supports wheel.
* Applies pep257 and fixes the violations.

0.9.1 (2015-03-17)
^^^^^^^^^^^^^^^^^^

* Fail creating object from stdin.

0.9.0 (2015-03-12)
^^^^^^^^^^^^^^^^^^

* Changed using swiftsc.Client().

  * This is supported swiftsc >= 0.6.0.

* Supported PyPy.
* Fixed some issues.

0.8.4 (2014-11-19)
^^^^^^^^^^^^^^^^^^

* Supported timeout option.

0.8.3 (2014-11-16)
^^^^^^^^^^^^^^^^^^

* Fixed #20 "rotate_limit" seems not to work.
* Unsupported Python3.2, PyPy.
* Appended pass through tox from python setup.py test.
* Integrated pylint, pychecker, pep8, flakes to Tox.
* Fixed violation of pylint.
* Fixed argument of exception at backup_file method.

0.8.2 (2014-05-10)
^^^^^^^^^^^^^^^^^^

* Refactoring.
* Apply tox for unit test.
* Support Python 3.4, PyPI.

0.8.1 (2014-01-10)
^^^^^^^^^^^^^^^^^^

* Append Python 3 classifier to setup.py
* Refine description.
    
  * Thanks, Thomas Goirand.

* Bug fix

  * ImportError: No module named magic in travis-ci

0.8 (2013-07-27)
^^^^^^^^^^^^^^^^

* read the file from stdin pipe
* Omitted option of --container

0.7 (2013-06-14)
^^^^^^^^^^^^^^^^

* support Python 3.2, 3.3

0.6 (2013-06-03)
^^^^^^^^^^^^^^^^

* support authentication of keystone

0.5 (2013-05-30)
^^^^^^^^^^^^^^^^

* New features

  * upload / retrieve / delete in parallel
  * support to delete multiple objects

* Bug fix

  * fixes fail to raise IOError if default config file exists
  * fail to use "rotate_limit" option on configuration file
  * support pep8 less than version 1.3

0.4 (2013-05-29)
^^^^^^^^^^^^^^^^

* New features

  * support default config file 
  * specify any container
  * support to retrieve multiple objects
  * specify multiple upload files

* Bug fix

  * fixes spelling error
  * remove pychecker for travis

0.3.2 (2013-05-24)
^^^^^^^^^^^^^^^^^^

* fixes fail backup and rotate with verifing default SSL certificate

0.3.1 (2013-05-20)
^^^^^^^^^^^^^^^^^^

* add option to ignore verifing of SSL certificate

0.3 (2013-05-17)
^^^^^^^^^^^^^^^^

* add retrieve backup object command

0.2 (2013-05-10)
^^^^^^^^^^^^^^^^

* add backup object command
* fixes man manual

0.1.3 (2013-05-10)
^^^^^^^^^^^^^^^^^^

* applied changing api of swiftsc.client.is_container()
* add how to setup and usage

0.1.2 (2013-05-09)
^^^^^^^^^^^^^^^^^^

* fixes #3 failed to execute in python2.6

0.1.1 (2013-05-08)
^^^^^^^^^^^^^^^^^^

* fixes #1 fail to execute firstly when there is no container

0.1 (2013-05-08)
^^^^^^^^^^^^^^^^

* first release


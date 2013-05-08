==============================================
backup2swift is backup data to OpenStack Swift
==============================================

This tool is that backup data to OpenStack Swift. provides features are command line interface, and backup rotatition.
This tool is depend on swiftsc, that is simple client library of OpenStack Swift.


Requirements
------------

* Python 2.7 or Python 3.2
* swift 0.1.1 lator


Setup
-----
::

   $ git clone https://github.com/mkouhei/backup2swift
   $ cd backup2swift
   $ sudo python setup.py install


Contribute
----------

Firstly copy pre-commit hook script.::

   $ cp -f utils/pre-commit.txt .git/hooks/pre-commit

Next install python2.7 later, and python-swiftsc, py.test. Below in Debian GNU/Linux Sid system,::

   $ sudo apt-get install python python-swiftsc python-pytest pep8

Then checkout 'devel' branch for development, commit your changes. Before pull request, execute git rebase.


See also
--------

* `OpenStack Object Storage Developer Guide <http://docs.openstack.org/api/openstack-object-storage/1.0/content/index.html>`_
* `swiftsc <https://github.com/mkouhei/swiftsc>`_


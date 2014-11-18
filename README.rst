==============================================
backup2swift is backup data to OpenStack Swift
==============================================

This utility is used to backup data to OpenStack Swift.
It provides a command interface and backup rotation.
It depends on a simple client library called swiftsc.

.. image:: https://secure.travis-ci.org/mkouhei/backup2swift.png?branch=devel
   :target: http://travis-ci.org/mkouhei/backup2swift
.. image:: https://coveralls.io/repos/mkouhei/backup2swift/badge.png?branch=devel
   :target: https://coveralls.io/r/mkouhei/backup2swift?branch=devel
.. image:: https://pypip.in/v/backup2swift/badge.png
   :target: https://crate.io/packages/backup2swift

Requirements
------------

* Python 2.7 later or Python 3.3 later
* swiftsc 0.5.5 later


Setup
-----
::

   $ git clone https://github.com/mkouhei/backup2swift
   $ cd backup2swift
   $ sudo python setup.py install

or via PyPI::

  $ virtualenv --no-site-packages venv
  $ pip install backup2swift

Usage
-----

Firstly setup configuration file. You may save the file name of your choice as setting. Example is as folloing::

  [swift]
  auth_url: https://example.org/auth/v1.0
  username: username
  password: password
  #ignore_verify_ssl_certification: True
  #timeout: 5.0

  [backup]
  rotate_limit: 10

  #[keystone]
  #tenant_id: tenant_id

The "auth_url" is swift authentication url, "username" and "password" are swift's. If you need to ignore verification of SSL certification, append option as "ignore_verify_ssl_certification: True" to [swift] section. "rotate_limit" is limitation count of rotation for backup. If this value is 3,  backup is as folloing;

backup target file name: example.txt

Firstly backup object is created as same name of backup target file (that is "example.txt")::

   $ bu2sw -c bu2sw.conf -p example.txt
   $ bu2sw -c bu2sw.conf -l
   example.txt

Secondly backup object is created as same name of backup target file, and first backup object is renamed added timestamp as "example.txt_YYYYMMDD-hhmmss".::

   $ bu2sw -c bu2sw.conf -p example.txt
   $ bu2sw -c bu2sw.conf -l
   example.txt
   example.txt_20130510-113930

Backup objects named with timestamp are created until "rotate_limit" value. Old backup object is remove when execute backup over limitation.::

   $ bu2sw -c bu2sw.conf -p example.txt
   $ bu2sw -c bu2sw.conf -l
   example.txt
   example.txt_20130510-113930
   example.txt_20130510-113941
   example.txt_20130510-113953
   $ bu2sw -c bu2sw.conf -p example.txt
   $ bu2sw -c bu2sw.conf -l
   example.txt
   example.txt_20130510-113941
   example.txt_20130510-113953
   example.txt_20130510-114110

See also man manual of bu2sw(1).

Contribute
----------

Firstly copy pre-commit hook script.::

   $ cp -f utils/pre-commit.txt .git/hooks/pre-commit

Next install python2.6 later, and python-swiftsc, py.test. Below in Debian GNU/Linux Sid system,::

   $ sudo apt-get install python python-swiftsc python-pytest pep8

Then checkout 'devel' branch for development, commit your changes. Before pull request, execute git rebase.


See also
--------

* `OpenStack Object Storage Developer Guide <http://docs.openstack.org/api/openstack-object-storage/1.0/content/index.html>`_
* `swiftsc <https://github.com/mkouhei/swiftsc>`_


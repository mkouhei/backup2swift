==============================================
backup2swift is backup data to OpenStack Swift
==============================================

This utility is used to backup data to OpenStack Swift.
It provides a command interface and backup rotation.
It depends on a simple client library called swiftsc.

.. image:: https://secure.travis-ci.org/mkouhei/backup2swift.png?branch=master
   :target: http://travis-ci.org/mkouhei/backup2swift
.. image:: https://coveralls.io/repos/mkouhei/backup2swift/badge.png?branch=master
   :target: https://coveralls.io/r/mkouhei/backup2swift?branch=master
.. image:: https://img.shields.io/pypi/v/backup2swift.svg
   :target: https://pypi.python.org/pypi/backup2swift

Requirements
------------

* Python 2.7 later or Python 3.3 later
* swiftsc 0.6.3 later


Setup
-----
::

   $ pip install --user backup2swift
   or
   (venv)$ pip install backup2swift

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

See also
--------

* `OpenStack Object Storage Developer Guide <http://docs.openstack.org/api/openstack-object-storage/1.0/content/index.html>`_
* `swiftsc <https://github.com/mkouhei/swiftsc>`_


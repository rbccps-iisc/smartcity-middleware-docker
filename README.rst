=================================================================
IoT Data Exchange & Analytics Middleware (IDEAM) for Smart Cities
=================================================================

.. image:: https://travis-ci.org/rbccps-iisc/ideam.svg?branch=master
    :target: https://travis-ci.org/rbccps-iisc/ideam

Web Page
========
- Main Page: https://smartcity.rbccps.org/
- About: http://www.rbccps.org/smart-city/
- Middleware API Documentation: https://rbccps-iisc.github.io/
- Tools and SDK's: https://github.com/rbccps-iisc/ideam-python-sdk

Architecture
============
.. image:: https://rbccps.org/smartcity/lib/exe/fetch.php?media=mw_architecture.png

Requirements
============
- ``Docker``: `Installation steps for Docker in Ubuntu/Debian <https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#os-requirements>`_ 
- ``Ansible``: `Installation steps for Ansible <http://docs.ansible.com/ansible/latest/intro_installation.html>`_
- ``ssh-keygen``: Generate a RSA Key Pair for the user who will install the script.


Release
=======

ideam v1.0.0_

Use the ideam deb file to install in Linux machines after satisfying the requirements. ``dpkg -i ideam.deb`` .


.. _v1.0.0: https://github.com/rbccps-iisc/ideam/releases/latest

Configuration
=============

ideam.conf_ v1.0.0

- Config file is located at ``/etc/ideam/ideam.conf``.

- The data files or docker persistent storage is at ``/var/ideam/data`` directory.

- The persistent storage can be changed by modifying the ``ideam.conf`` before installation.

.. _ideam.conf: https://github.com/rbccps-iisc/ideam/blob/master/ideam.conf


Steps to Install
================

After downloading and installing the deb file, do the following steps.

+---------------------------------------+-----------------------------------------------------------------------------+
| Installation                          | ``ideam install``   or if you cloned ``./ideam install``                    |
+---------------------------------------+-----------------------------------------------------------------------------+
| Start Ideam                           | ``ideam start``    or if you cloned ``./ideam start``                       |
+---------------------------------------+-----------------------------------------------------------------------------+
| Serving Ideam at                      | ``https://localhost:10443``                                                 |
+---------------------------------------+-----------------------------------------------------------------------------+

- The application will be serving with a self-signed certificate.
  If you want to use your certificate, have your .crt and .key file as ``/usr/share/ideam/config/kong/default_443.crt`` and
  ``/usr/share/ideam/config/kong/default_443.key`` respectively and do a fresh installation.

- If installation fails at some instance, all the time-dated logs are available at ``/tmp/ideam-%Y-%m-%d-%H-%M.log``.



Comment
=======

+----------------------------------------------------------------+----------------------------------------------------------+
| RBCCPS IoT MIDDLEWARE IDEAM API URL                            | INSTALLED IOT MIDDLEWARE IDEAM API URLs                  |
+================================================================+==========================================================+
| https://smartcity.rbccps.org/api/1.0.0/register                | https://localhost:10443/api/1.0.0/register               |
+----------------------------------------------------------------+----------------------------------------------------------+
| https://smartcity.rbccps.org/api/1.0.0/publish                 | https://localhost:10443/api/1.0.0/publish                |
+----------------------------------------------------------------+----------------------------------------------------------+
| https://smartcity.rbccps.org/api/1.0.0/subscribe?name=testDemo | https://localhost:10443/api/1.0.0/subscribe?name=testDemo|
+----------------------------------------------------------------+----------------------------------------------------------+
| https://smartcity.rbccps.org/api/1.0.0/follow                  | https://localhost:10443/api/1.0.0/follow                 |
+----------------------------------------------------------------+----------------------------------------------------------+
| https://smartcity.rbccps.org/api/1.0.0/cat                     | https://localhost:10443/api/1.0.0/cat                    |
+----------------------------------------------------------------+----------------------------------------------------------+
| https://smartcity.rbccps.org/api/1.0.0/db                      | https://localhost:10443/api/1.0.0/db                     |
+----------------------------------------------------------------+----------------------------------------------------------+

NOTE
====
- Installation in Linux machines can fail for the following reasons.
    - If you are in a corporate network that blocks Google DNS Servers, the ``ideam install`` command fails.

      To fix it, add your corporate DNS servers in DOCKER_OPTS in /etc/default/docker. (for SysV machines)

         DOCKER_OPTS="--dns 208.67.222.222 --dns 208.67.220.220"

      If this fails to set the DNS properly, try updating /etc/docker/daemon.json with the following (for systemd machines)

         { "dns": ["208.67.222.222", "208.67.220.220"] }

- IDEAM has been tested on MacOS as well.
    

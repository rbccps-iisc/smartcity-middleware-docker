=================================================================
IoT Data Exchange & Analytics Middleware (IDEAM) for Smart Cities
=================================================================

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
- ``Python-pip``: Python package dependency (pathlib2). Use the command ``python -m pip install pathlib2``
- ``ssh-keygen``: Generate a RSA Key Pair for the user who will install the script.
 
Release
=======

smartcity-middleware v1.0.0_


.. _v1.0.0: https://github.com/rbccps-iisc/ideam/releases/latest

Configuration
=============

middleware.conf_ v0.1.0

.. _middleware.conf: https://github.com/rbccps-iisc/ideam/blob/master/middleware.conf
middleware.conf::

      DESCRIPTION

      middleware.conf is the configuration file for the smartcity-middleware application.

      KONG, RABBITMQ, TOMCAT, CATALOGUE, LDAP docker containers requires a persistent data, config storage locations.

      DATA_STORAGE: Specify an empty directory in the system that docker could use
      for keeping data files. Here, providing separate directories for kong, rabbitmq,
      tomcat, catalogue is recommended. Give all user rwx permission to these directories.

      CONFIG_STORAGE: Specify an empty directory in the system that docker could use
      for keeping config files.

      LOG_LOCATION: Specify an empty directory in the system that docker could use
      for keeping log files.

      SSH and other service ports can be mapped to host machine ports.

      SYSTEM_CONFIG specify system specific configurations for the installation steps.

      SSH_PUBLIC_KEY: Specify a ssh public key which will be used in ssh authentication of the user to
      docker containers.


Steps to Install
================

After configuring the ``middleware.conf`` file, do the following steps.

+---------------------------------------+-----------------------------------------------------------------------------+
| Installation                          | ``python smartcity-middleware.py install --config-file middleware.conf``    |
+---------------------------------------+-----------------------------------------------------------------------------+
| Start Middleware                      | ``python smartcity-middleware.py start``                                    |
+---------------------------------------+-----------------------------------------------------------------------------+
| Serving Middleware at                 | ``https://localhost:10443``                                                 |
+---------------------------------------+-----------------------------------------------------------------------------+



Comment
=======
- Please satisfy the requirements mentioned in ``middleware.conf`` file.
- Password of the root user in docker containers for the 1.0.0 release is rbccps@123456. This will be removed in the later release.
- If the setup fails at any stage for reasons like internet connection issues, you can continue the failed installation using the following command.
     ``python smartcity-middleware.py install --config-file middleware.conf -l kong,tomcat,hypercat,ldapd,elasticsearch,rabbitmq,apt_repo,pushpin``
- The application will be serving with a self-signed certificate. If you want to use your certificate, have your .crt and .key file as ``config/kong/default_443.crt`` and ``config/kong/default_443.key`` respectively and do a fresh installation.

+----------------------------------------------------------------+----------------------------------------------------------+
| RBCCPS MIDDLEWARE API URLs                                     | MIDDLEWARE API URLs                                      |
+================================================================+==========================================================+
| https://smartcity.rbccps.org/api/1.0.0/register                | https://localhost:10443/api/1.0.0/register               |
+----------------------------------------------------------------+----------------------------------------------------------+
| https://smartcity.rbccps.org/api/1.0.0/publish                 | https://localhost:10443/api/1.0.0/publish                |
+----------------------------------------------------------------+----------------------------------------------------------+
| https://smartcity.rbccps.org/api/1.0.0/subscribe?name=testDemo | https://localhost:10443/api/1.0.0/subscribe?name=testDemo|
+----------------------------------------------------------------+----------------------------------------------------------+
| https://smartcity.rbccps.org/api/1.0.0/subscribe/bind          | https://localhost:10443/api/1.0.0/subscribe/bind         |
+----------------------------------------------------------------+----------------------------------------------------------+
| https://smartcity.rbccps.org/api/1.0.0/subscribe/unbind        | https://localhost:10443/api/1.0.0/subscribe/unbind       |
+----------------------------------------------------------------+----------------------------------------------------------+
| https://smartcity.rbccps.org/api/1.0.0/cat                     | https://localhost:10443/api/1.0.0/cat                    |
+----------------------------------------------------------------+----------------------------------------------------------+
| https://smartcity.rbccps.org/api/1.0.0/historicData            | https://localhost:10443/api/1.0.0/historicData           |
+----------------------------------------------------------------+----------------------------------------------------------+

For example, registration of device to local middleware is as follows.

``curl -i -X GET "https://localhost:10443/api/0.1.0/register" -H 'apikey: <provider_api_key>' -H 'resourceID: <Your-Resource-ID>' -H 'serviceType: publish,subscribe,historicData'`` 


NOTE
====
- Installation in Linux machines can fail for the following reasons.
    - If you are in a corporate network that blocks Google DNS Servers, the ``docker build`` command fails.
      
      To fix it, add your corporate DNS servers in DOCKER_OPTS in /etc/default/docker. (for SysV machines)

         DOCKER_OPTS="--dns 208.67.222.222 --dns 208.67.220.220" 

      If this fails to set the DNS properly, try updating /etc/docker/daemon.json with the following (for systemd machines)

         { "dns": ["208.67.222.222", "208.67.220.220"] } 

    - Middleware has been tested on macOS as well.
    

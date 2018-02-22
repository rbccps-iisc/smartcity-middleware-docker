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

middleware.conf_ v1.0.0

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
| https://smartcity.rbccps.org/api/1.0.0/follow                  | https://localhost:10443/api/1.0.0/follow                 |
+----------------------------------------------------------------+----------------------------------------------------------+
| https://smartcity.rbccps.org/api/1.0.0/cat                     | https://localhost:10443/api/1.0.0/cat                    |
+----------------------------------------------------------------+----------------------------------------------------------+
| https://smartcity.rbccps.org/api/1.0.0/db                      | https://localhost:10443/api/1.0.0/db                     |
+----------------------------------------------------------------+----------------------------------------------------------+

For example, registration of device to local middleware is as follows.

command::

      curl -X POST \
        https://smartcity.rbccps.org/api/1.0.0/register \
        -H 'apikey: guest' \
        -d '{
        "entitySchema": {
          "refCatalogueSchema": "generic_iotdevice_schema.json",
          "resourceType": "streetlight",
          "tags": ["onstreet", "Energy", "still under development!"],
          "refCatalogueSchemaRelease": "0.1.0",
          "latitude": {
            "value": 13.0143335,
            "ontologyRef": "http://www.w3.org/2003/01/geo/wgs84_pos#"
          },
          "longitude": {
            "value": 77.5678424,
            "ontologyRef": "http://www.w3.org/2003/01/geo/wgs84_pos#"
          },
          "owner": {
            "name": "IISC",
            "website": "http://www.iisc.ac.in"
          },
          "provider": {
            "name": "Robert Bosch Centre for Cyber Physical Systems, IISc",
            "website": "http://rbccps.org"
          },
          "geoLocation": {
            "address": "80 ft Road, Bangalore, 560012"
          },
          "data_schema": {
            "type": "object",
            "properties": {
              "dataSamplingInstant": {
                "type": "number",
                "description": "Sampling Time in EPOCH format",
                "units": "seconds",
                "permissions": "read",
                "accessModifier": "public"
              },
              "caseTemperature": {
                "type": "number",
                "description": "Temperature of the device casing",
                "units": "degreeCelsius",
                "permissions": "read",
                "accessModifier": "public"
              },
              "powerConsumption": {
                "type": "number",
                "description": "Power consumption of the device",
                "units": "watts",
                "permissions": "read",
                "accessModifier": "public"
              },
              "luxOutput": {
                "type": "number",
                "description": "lux output of LED measured at LED",
                "units": "lux",
                "permissions": "read",
                "accessModifier": "public"
              },
              "ambientLux": {
                "type": "number",
                "description": "lux value of ambient",
                "units": "lux",
                "permissions": "read",
                "accessModifier": "public"
              },
              "targetPowerState": {
                "type": "string",
                "enum": ["ON", "OFF"],
                "units": "dimensionless",
                "description": "If set to ON, turns ON the device. If OFF turns OFF the device. Writeable parameter. Writeable only allowed for authorized apps",
                "permissions": "read-write",
                "accessModifier": "protected"
              },
              "targetBrightnessLevel": {
                "type": "number",
                "description": "Number between 0 to 100 to indicate the percentage brightness level. Writeable only allowed for authorized apps",
                "units": "percent",
                "permissions": "read-write",
                "accessModifier": "protected"
              },
              "targetControlPolicy": {
                "enum": ["AUTO_TIMER", "AUTO_LUX", "MANUAL"],
                "units": "dimensionless",
                "permissions": "read-write",
                "description": "Indicates which of the behaviours the device should implement. AUTO_TIMER is timer based, AUTO_LUX uses ambient light and MANUAL is controlled by app. Writeable only allowed for authorized apps",
                "accessModifier": "protected"
              },
              "targetAutoTimerParams": {
                "type": "object",
                "permissions": "read-write",
                "properties": {
                  "targetOnTime": {
                    "type": "number",
                    "description": "Indicates time of day in seconds from 12 midnight when device turns ON in AUTO_TIMER. Writeable only allowed for authorized apps",
                    "units": "seconds",
                    "accessModifier": "protected"
                  },
                  "targetOffTime": {
                    "type": "number",
                    "description": "Indicates time of day in seconds from 12 midnight when device turns OFF in AUTO_TIMER. Writeable only allowed for authorized apps",
                    "units": "seconds",
                    "accessModifier": "protected"
                  }
                }
              },
              "targetAutoLuxParams": {
                "type": "object",
                "permissions": "read-write",
                "properties": {
                  "targetOnLux": {
                    "type": "number",
                    "description": "Indicates ambient lux when device turns ON in AUTO_LUX. Writeable only allowed for authorized apps",
                    "units": "lux",
                    "accessModifier": "protected"
                  },
                  "targetOffLux": {
                    "type": "number",
                    "description": "Indicates ambient lux when device turns OFF in AUTO_LUX. Writeable only allowed for authorized apps",
                    "units": "lux",
                    "accessModifier": "protected"
                  }
                }
              }
            },
            "additionalProperties": false
          },
          "serialization_from_device": {
            "format": "protocol-buffers",
            "schema_ref": {
              "type": "proto 2",
              "mainMessageName": "sensor_values",
              "link": "https://raw.githubusercontent.com/rbccps-iisc/applications-streetlight/master/proto_stm/txmsg/sensed.proto"
            }
          },
          "serialization_to_device": {
            "format": "protocol-buffers",
            "schema_ref": {
              "type": "proto 2",
              "mainMessageName": "targetConfigurations",
              "link": "https://raw.githubusercontent.com/rbccps-iisc/applications-streetlight/master/proto_stm/rxmsg/actuated.proto"
            }
          },
          "id": "streetLight_1A_212"
        }
      }'


NOTE
====
- Installation in Linux machines can fail for the following reasons.
    - If you are in a corporate network that blocks Google DNS Servers, the ``docker build`` command fails.
      
      To fix it, add your corporate DNS servers in DOCKER_OPTS in /etc/default/docker. (for SysV machines)

         DOCKER_OPTS="--dns 208.67.222.222 --dns 208.67.220.220" 

      If this fails to set the DNS properly, try updating /etc/docker/daemon.json with the following (for systemd machines)

         { "dns": ["208.67.222.222", "208.67.220.220"] } 

    - Middleware has been tested on macOS as well.
    

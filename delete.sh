#!/usr/bin/env bash
cd /data/kong && sudo rm -rf *
cd /data/tomcat && sudo rm -rf *
cd /data/rabbitmq && sudo rm -rf *
cd /data/ldapd && sudo rm -rf *
cd /data/logs/kong && sudo rm -rf *
cd /data/logs/rabbitmq && sudo rm -rf *
cd /data/logs/tomcat && sudo rm -rf *

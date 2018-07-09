#!/bin/bash

echo -e "\nCopying CA user certifiate key"
docker cp config/certificate_authority/keys/ca-user-certificate-key.pub tomcat:/etc/ssh/ca-user-certificate-key.pub
docker exec -i tomcat mkdir -p /root/.ssh/ 

echo -e "\nAdding user's SSH public key into authorised keys"
docker exec -i tomcat dd of=/root/.ssh/authorized_keys < ~/.ssh/id_rsa.pub > /dev/null 2>&1

echo -e "\nCopying RegisterAPI.war into tomcat webapps folder"
docker cp config/tomcat/RegisterAPI.war tomcat:/usr/local/tomcat/webapps 

echo -e "\nCopying setup script into tomcat container"
docker cp tasks/tomcat/quick-tomcat-setup.sh tomcat:/etc/

echo -e "\nAdding necessary permissions to files and folders needed by Tomcat"
docker exec tomcat chmod +x /etc/quick-tomcat-setup.sh

echo -e "\nStarting setup script"
docker exec tomcat /etc/quick-tomcat-setup.sh 

echo -e "\nCopying RabbitMQ and LDAP passwords"
docker cp config/tomcat/pwd tomcat:/etc/pwd
docker cp config/tomcat/rmqpwd tomcat:/etc/rmqpwd

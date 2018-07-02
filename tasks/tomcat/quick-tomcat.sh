#!/bin/bash
docker cp config/certificate_authority/keys/ca-user-certificate-key.pub tomcat:/etc/ssh/ca-user-certificate-key.pub
docker exec -i tomcat mkdir -p /root/.ssh/ 
docker exec -i tomcat dd of=/root/.ssh/authorized_keys < ~/.ssh/id_rsa.pub > /dev/null 2>&1
#sshpass -p "rbccps@123456" ssh root@localhost -p $1 < tasks/tomcat/quick-tomcat-setup.sh 
docker cp config/tomcat/RegisterAPI.war tomcat:/usr/local/tomcat/webapps 
docker cp tasks/tomcat/quick-tomcat-setup.sh tomcat:/etc/
docker exec tomcat chmod +x /etc/quick-tomcat-setup.sh
docker exec tomcat /etc/quick-tomcat-setup.sh 
docker cp config/tomcat/pwd tomcat:/etc/pwd
docker cp config/tomcat/rmqpwd tomcat:/etc/rmqpwd

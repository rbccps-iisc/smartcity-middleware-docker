#!/bin/bash
docker cp config/certificate_authority/keys/ca-user-certificate-key.pub tomcat:/etc/ssh/ca-user-certificate-key.pub
docker exec -i tomcat mkdir -p /root/.ssh/ 
docker exec -i tomcat dd of=/root/.ssh/authorized_keys < ~/.ssh/id_rsa.pub
sshpass -p "rbccps@123456" ssh root@localhost -p $1 < tasks/tomcat/quick-tomcat-setup.sh 
docker cp config/tomcat/pwd tomcat:/etc/pwd
docker cp config/tomcat/rmqpwd tomcat:/etc/rmqpwd

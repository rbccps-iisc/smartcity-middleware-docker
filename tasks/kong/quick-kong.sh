#!/bin/bash
docker cp config/certificate_authority/keys/ca-user-certificate-key.pub kong:/etc/ssh/ca-user-certificate-key.pub
docker exec -i kong mkdir -p /root/.ssh/ 
docker exec -i kong dd of=/root/.ssh/authorized_keys < ~/.ssh/id_rsa.pub
docker cp host_vars/rabbitmq kong:/etc
docker cp host_vars/ldapd kong:/etc
sshpass -p "rbccps@123456" ssh root@localhost -p $1 < tasks/kong/quick-kong-setup.sh 

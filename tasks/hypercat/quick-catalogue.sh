#!/bin/bash
docker cp config/certificate_authority/keys/ca-user-certificate-key.pub catalogue:/etc/ssh/ca-user-certificate-key.pub
docker exec -i catalogue mkdir -p /root/.ssh/ 
docker exec -i catalogue dd of=/root/.ssh/authorized_keys < ~/.ssh/id_rsa.pub
sshpass -p "rbccps@123456" ssh root@localhost -p $1 < tasks/hypercat/quick-catalogue-setup.sh 

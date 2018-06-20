#!/bin/bash
docker cp config/certificate_authority/keys/ca-user-certificate-key.pub kong:/etc/ssh/ca-user-certificate-key.pub
docker exec -i kong mkdir -p /root/.ssh/ 
docker exec -i kong dd of=/root/.ssh/authorized_keys < ~/.ssh/id_rsa.pub
sshpass -p "rbccps@123456" ssh root@localhost -p $1 < tasks/kong/quick-kong-setup.sh 

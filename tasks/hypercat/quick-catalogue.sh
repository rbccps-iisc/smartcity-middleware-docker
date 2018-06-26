#!/bin/bash
docker cp config/certificate_authority/keys/ca-user-certificate-key.pub hypercat:/etc/ssh/ca-user-certificate-key.pub
docker exec -i hypercat mkdir -p /root/.ssh/ 
docker exec -i hypercat dd of=/root/.ssh/authorized_keys < ~/.ssh/id_rsa.pub
docker cp host_vars/ldapd hypercat:/etc/
sshpass -p "rbccps@123456" ssh root@localhost -p $1 < tasks/hypercat/quick-catalogue-setup.sh 

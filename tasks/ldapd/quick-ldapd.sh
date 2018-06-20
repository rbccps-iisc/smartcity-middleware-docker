#!/bin/bash
docker cp config/certificate_authority/keys/ca-user-certificate-key.pub ldapd:/etc/ssh/ca-user-certificate-key.pub
docker exec -i ldapd mkdir -p /root/.ssh/ 
docker exec -i ldapd dd of=/root/.ssh/authorized_keys < ~/.ssh/id_rsa.pub
sshpass -p "rbccps@123456" ssh root@localhost -p $1 < tasks/ldapd/quick-ldapd-setup.sh 

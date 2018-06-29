#!/bin/bash
docker cp config/certificate_authority/keys/ca-user-certificate-key.pub ldapd:/etc/ssh/ca-user-certificate-key.pub
docker exec -i ldapd mkdir -p /root/.ssh/ 
docker exec -i ldapd dd of=/root/.ssh/authorized_keys < ~/.ssh/id_rsa.pub > /dev/null 2>&1
docker cp host_vars/ldapd ldapd:/etc/
#sshpass -p "rbccps@123456" ssh root@localhost -p $1 < tasks/ldapd/quick-ldapd-setup.sh 
docker cp tasks/ldapd/quick-ldapd-setup.sh ldapd:/etc/
docker exec ldapd chmod +x /etc/quick-ldapd-setup.sh
docker exec ldapd /etc/quick-ldapd-setup.sh 

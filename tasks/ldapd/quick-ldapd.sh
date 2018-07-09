#!/bin/bash

echo -e "\nCopying CA user certifiate key"
docker cp config/certificate_authority/keys/ca-user-certificate-key.pub ldapd:/etc/ssh/ca-user-certificate-key.pub
docker exec -i ldapd mkdir -p /root/.ssh/ 

echo -e "\nAdding user's SSH public key into authorised keys"
docker exec -i ldapd dd of=/root/.ssh/authorized_keys < ~/.ssh/id_rsa.pub > /dev/null 2>&1

echo -e "\nCopying LDAP password"
docker cp host_vars/ldapd ldapd:/etc/

echo -e "\nCopying setup script"
docker cp tasks/ldapd/quick-ldapd-setup.sh ldapd:/etc/

echo -e "\nAdding necessary permissions to files and folders needed by LDAP"
docker exec ldapd chmod +x /etc/quick-ldapd-setup.sh

echo -e "\nStarting setup script"
docker exec ldapd /etc/quick-ldapd-setup.sh 

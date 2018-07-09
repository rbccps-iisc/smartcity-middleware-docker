#!/bin/bash

echo -e "\nCopying CA user certifiate key"
docker cp config/certificate_authority/keys/ca-user-certificate-key.pub hypercat:/etc/ssh/ca-user-certificate-key.pub
docker exec -i hypercat mkdir -p /root/.ssh/ 

echo -e "\nAdding user's SSH public key into authorised keys"
docker exec -i hypercat dd of=/root/.ssh/authorized_keys < ~/.ssh/id_rsa.pub > /dev/null 2>&1

echo -e "\nCopying LDAP password"
docker cp host_vars/ldapd hypercat:/etc/

echo -e "\nCopying setup script"
docker cp tasks/hypercat/quick-catalogue-setup.sh hypercat:/etc/

echo -e "\nAdding necessary permissions to files and folders needed by catalogue"
docker exec hypercat chmod +x /etc/quick-catalogue-setup.sh

echo -e "\nStarting setup script"
docker exec hypercat /etc/quick-catalogue-setup.sh 

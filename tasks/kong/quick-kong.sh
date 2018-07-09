#!/bin/bash

echo -e "\nCopying CA user certifiate key"
docker cp config/certificate_authority/keys/ca-user-certificate-key.pub kong:/etc/ssh/ca-user-certificate-key.pub
docker exec -i kong mkdir -p /root/.ssh/ 

echo -e "\nAdding user's SSH public key into authorised keys"
docker exec -i kong dd of=/root/.ssh/authorized_keys < ~/.ssh/id_rsa.pub > /dev/null 2>&1

echo -e "\nCopying RabbitMQ and LDAP password"
docker cp host_vars/rabbitmq kong:/etc
docker cp host_vars/ldapd kong:/etc

echo -e "\nCopying setup script into kong container"
docker cp tasks/kong/quick-kong-setup.sh kong:/etc/

echo -e "\nAdding necessary permissions to files and folders needed by kong"
docker exec kong chmod 777 /etc/quick-kong-setup.sh
docker exec kong chmod -R 777 /var/lib/postgresql 
docker exec kong chmod -R 777 /tmp

echo -e "\nStarting setup script"
docker exec kong /etc/quick-kong-setup.sh

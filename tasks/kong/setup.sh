#!/bin/bash
RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'

#echo -e "${YELLOW}[  INFO  ] ${NC}Copying CA user certifiate key"

#docker cp config/certificate_authority/keys/ca-user-certificate-key.pub kong:/etc/ssh/ca-user-certificate-key.pub

#if [ $? -eq 0 ]; then
#    echo -e "${GREEN}[   OK   ] ${NC}Copied certificate key"
#else
#    echo -e "${RED}[ ERROR ] ${NC}Failed to copied certificate key"
#fi

docker exec -i kong mkdir -p /root/.ssh/ 

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC}Created .ssh directory in /root"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to create .ssh directory in /root" 
fi

echo -e "${YELLOW}[  INFO  ] ${NC}Adding user's SSH public key into authorised keys"

docker exec -i kong dd of=/root/.ssh/authorized_keys < ~/.ssh/id_rsa.pub > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC}Added user's SSH public key"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to add user's SSH public key into authorised keys"
fi

echo -e "${YELLOW}[  INFO  ] ${NC}Copying RabbitMQ and LDAP password"

docker cp host_vars/rabbitmq kong:/etc
docker cp host_vars/ldapd kong:/etc

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC}Copied passwords"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to copy RabbitMQ and LDAP passwords"
fi

echo -e "${YELLOW}[  INFO  ] ${NC}Copying setup script into kong container"

docker cp tasks/kong/install.sh kong:/etc/

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC}Copied setup script"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to copy setup script into Kong container"
fi

echo -e "${YELLOW}[  INFO  ] ${NC}Adding necessary permissions to files and folders needed by kong"
#TODO give necessary permissions only to the required user

docker exec kong chmod 777 /etc/install.sh
docker exec kong chmod -R 777 /var/lib/postgresql 
docker exec kong chmod -R 777 /tmp

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC}Added necessary permissions"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to add permissions to file(s)"
fi

echo -e "${YELLOW}[  INFO  ] ${NC}Starting setup script"

docker exec kong /etc/install.sh

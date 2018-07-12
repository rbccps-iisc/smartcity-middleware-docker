#!/bin/bash

RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'

echo -e "${YELLOW}[  INFO  ]${NC} Copying CA user certifiate key"

docker cp config/certificate_authority/keys/ca-user-certificate-key.pub tomcat:/etc/ssh/ca-user-certificate-key.pub

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC}Copied certificate key"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to copied certificate key"
fi

docker exec -i tomcat mkdir -p /root/.ssh/ 

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC}Created .ssh directory in /root"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to create .ssh directory in /root" 
fi

echo -e "${YELLOW}[  INFO  ]${NC} Adding user's SSH public key into authorised keys"

docker exec -i tomcat dd of=/root/.ssh/authorized_keys < ~/.ssh/id_rsa.pub > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC}Added user's SSH public key"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to add user's SSH public key into authorised keys"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Copying RegisterAPI.war into tomcat webapps folder"

docker cp config/tomcat/RegisterAPI.war tomcat:/usr/local/tomcat/webapps 

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC}Copied war file"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to copy war file"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Copying setup script into tomcat container"

docker cp tasks/tomcat/quick-tomcat-setup.sh tomcat:/etc/

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC}Copied setup script"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to copy setup script into Kong container"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Adding necessary permissions to files and folders needed by Tomcat"

docker exec tomcat chmod +x /etc/quick-tomcat-setup.sh

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC}Added necessary permissions"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to add permissions to file(s)"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Starting setup script"

docker exec tomcat /etc/quick-tomcat-setup.sh 

echo -e "${YELLOW}[  INFO  ]${NC} Copying RabbitMQ and LDAP passwords"

docker cp config/tomcat/pwd tomcat:/etc/pwd
docker cp config/tomcat/rmqpwd tomcat:/etc/rmqpwd
echo -e "${GREEN}[   OK   ]${NC} Copied passwords"

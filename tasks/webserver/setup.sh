#!/bin/bash

RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'

echo -e "${YELLOW}[  INFO  ]${NC} Copying cdxapis.jar into webserver folder"

docker cp config/webserver/cdxapis.jar webserver:/usr/local/webserver

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC}Copied jar file"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to copy jar file"
fi


echo -e "${YELLOW}[  INFO  ]${NC} Copying cdxdatabase.jar into webserver folder"

docker cp config/webserver/cdxdatabase.jar webserver:/usr/local/webserver

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC}Copied jar file"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to copy jar file"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Copying setup script into webserver container"

docker cp tasks/webserver/install.sh webserver:/etc/

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC}Copied setup script"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to copy setup script into webserver container"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Adding necessary permissions to files and folders needed by Webserver"

docker exec webserver chmod +x /etc/install.sh

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC}Added necessary permissions"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to add permissions to file(s)"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Starting setup script"

docker exec webserver /etc/install.sh

echo -e "${YELLOW}[  INFO  ]${NC} Copying RabbitMQ and LDAP passwords"

docker cp config/webserver/pwd webserver:/etc/pwd

docker cp config/webserver/rmqpwd webserver:/etc/rmqpwd

echo -e "${GREEN}[   OK   ]${NC} Copied passwords"

#!/bin/bash
RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'

echo -e "${YELLOW}[  INFO  ] ${NC}Copying setup script into kong container"

docker cp tasks/apigateway/install.sh apigateway:/etc/

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC}Copied setup script"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to copy setup script into Kong container"
fi

echo -e "${YELLOW}[  INFO  ] ${NC}Copying API config file"

docker cp config/apigateway/config.yml apigateway:/etc/

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC}Copied config file"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to copy config file"
fi

echo -e "${YELLOW}[  INFO  ] ${NC}Adding necessary permissions to files and folders needed by kong"

#TODO give necessary permissions only to the required user

docker exec apigateway chmod +x /etc/install.sh

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC}Added necessary permissions"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to add permissions to file(s)"
fi

echo -e "${YELLOW}[  INFO  ] ${NC}Starting setup script"

docker exec apigateway /etc/install.sh

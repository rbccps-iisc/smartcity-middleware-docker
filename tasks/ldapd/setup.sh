#!/bin/bash

RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'

echo -e "${YELLOW}[  INFO  ]${NC} Copying LDAP password"

docker cp host_vars/ldapd ldapd:/etc/

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC}Copied passwords"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to copy RabbitMQ and LDAP passwords"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Copying setup script"

docker cp tasks/ldapd/install.sh ldapd:/etc/

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC}Copied setup script"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to copy setup script into ldapd container"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Copying ldapd script"

docker cp tasks/ldapd/ldapd.sh ldapd:/

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC}Copied ldapd script"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to copy ldapd script into ldapd container"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Adding necessary permissions to install script" 

docker exec ldapd chmod +x /etc/install.sh

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC}Added necessary permissions"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to add permissions to file(s)"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Adding necessary permissions to ldapd script" 

docker exec ldapd chmod +x ldapd.sh

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC}Added necessary permissions"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to add permissions to file(s)"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Starting setup script"

docker exec ldapd /etc/install.sh

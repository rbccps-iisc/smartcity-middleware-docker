#!/bin/bash

RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'

echo -e "${YELLOW}[  INFO  ]${NC} Copying LDAP password"

docker cp host_vars/ldapd catalogue:/etc/

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC}Copied password file"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to copy password file"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Copying setup script"

docker cp tasks/catalogue/install.sh catalogue:/etc/

echo -e "${YELLOW}[  INFO  ]${NC} Adding necessary permissions to files and folders needed by catalogue"

docker exec catalogue chmod +x /etc/install.sh

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC}Added necessary permissions"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to add permissions to file(s)"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Starting setup script"
docker exec catalogue /etc/install.sh

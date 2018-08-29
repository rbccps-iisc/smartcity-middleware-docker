#!/bin/ash

RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'

echo -e "${YELLOW}[  INFO  ]${NC} Installing admin scripts"

echo -e "${YELLOW}[  INFO  ]${NC} Creating admin.ideam user"

touch /usr/local/kong/consumer_error.log
touch /usr/local/kong/consumer_out.log

sh /usr/local/kong/setup/setup_consumer.sh admin.ideam 2>/usr/local/kong.consumer_error.log >/usr/local/kong/consumer_out.log

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC} Created admin.ideam user"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to create admin.ideam user"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Adding ACL to admin.ideam user"

touch /usr/local/kong/acl_error.log
touch /usr/local/kong/acl_out.log
sh /usr/local/kong/setup/setup_consumer-acl.sh admin.ideam 2>/usr/local/kong.acl_error.log >/usr/local/kong/acl_out.log

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC} Added ACL to admin.ideam user"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to add ACL to admin.ideam user"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Adding key-auth to admin.ideam user"

touch /usr/local/kong/auth_error.log
touch /usr/local/kong/auth_out.log

sh /usr/local/kong/setup/setup_consumer-key-auth.sh admin.ideam 2>/usr/local/kong.auth_error.log >/usr/local/kong/auth.log

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC}Added key-auth to admin.ideam user"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to add key-auth to admin.ideam user"
fi




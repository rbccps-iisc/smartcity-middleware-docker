#!/bin/ash

RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'

echo -e "${YELLOW}[  INFO  ]${NC} Installing admin scripts"

echo -e "${YELLOW}[  INFO  ]${NC} Creating cdx.admin user"

touch /usr/local/apigateway/consumer_error.log
touch /usr/local/apigateway/consumer_out.log

sh /usr/local/apigateway/setup/setup_consumer.sh cdx.admin 2>/usr/local/apigateway/consumer_error.log >/usr/local/apigateway/consumer_out.log

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC} Created cdx.admin user"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to create cdx.admin user"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Adding ACL to cdx.admin user"

touch /usr/local/apigateway/acl_error.log
touch /usr/local/apigateway/acl_out.log
sh /usr/local/apigateway/setup/setup_consumer-acl.sh cdx.admin 2>/usr/local/apigateway/acl_error.log >/usr/local/apigateway/acl_out.log

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC} Added ACL to cdx.admin user"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to add ACL to cdx.admin user"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Adding key-auth to cdx.admin user"

touch /usr/local/apigateway/auth_error.log
touch /usr/local/apigateway/auth_out.log

sh /usr/local/apigateway/setup/setup_consumer-key-auth.sh cdx.admin 2>/usr/local/apigateway/auth_error.log >/usr/local/apigateway/auth_out.log

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC}Added key-auth to cdx.admin user"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to add key-auth to cdx.admin user"
fi


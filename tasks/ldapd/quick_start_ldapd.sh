#!/bin/ash
  
RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'

if ! nc -z localhost 8389
then

echo -e "${YELLOW}[  INFO  ]${NC} Starting LDAP"

/usr/local/sbin/ldapd

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Started LDAP server"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to start LDAP server"
fi

else
echo -e "${YELLOW}[  INFO  ]${NC} LDAP is running"
fi

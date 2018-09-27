#!/bin/ash

RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'

pwd=`cat /etc/ldapd | cut -d : -f 2 | awk '{$1=$1};1'`

echo -e "${YELLOW}[  INFO  ]${NC} Changing passwords in files"

sed -i 's/ldap_pwd/'$pwd'/g' /etc/ldapd.conf

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Changed passwords"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to change passwords in files"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Starting LDAP"

tmux new-session -d -s ldapd './ldapd.sh'

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Started LDAP server"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to start LDAP server"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Waiting for LDAP to start up"

while ! nc -z localhost 8389
do
sleep 0.1
done

echo -e "${GREEN}[   OK   ]${NC} LDAP server is up"

echo -e "${YELLOW}[  INFO  ]${NC} Adding LDIF files"

ldapmodify -h 127.0.0.1 -p 8389 -x -D cn=admin,dc=smartcity -w $pwd -f /smartcity.ldif > /dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Added smartcity.ldif"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to add smartcity.ldif"
fi

ldapmodify -h 127.0.0.1 -p 8389 -x -D cn=admin,dc=smartcity -w $pwd -f /devices.ldif > /dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Added devices.ldif"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to add devices.ldif"
fi
rm /etc/ldapd

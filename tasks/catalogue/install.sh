#!/bin/ash

RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'

pwd=`cat /etc/ldapd | cut -d : -f 2 | awk '{$1=$1};1'`

echo -e "${YELLOW}[  INFO  ]${NC} Changing passwords in files"

sed -i 's/ldap_pwd/'$pwd'/g' /home/ideam/cat-json-schema-server/lib/config.js

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Changed passwords"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to change passwords in files"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Removing LDAP password file"

rm /etc/ldapd

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Deleted password file"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to delete password file"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Starting MongoDB"

tmux new-session -d -s mongo 'mongod'

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Started MongoDB"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to start MongoDB"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Waiting for MongoDB to start up"

while ! nc -z localhost 27017
do
sleep 0.1
done

echo -e "${YELLOW}[  INFO  ]${NC} MongoDb is up"

echo -e "${YELLOW}[  INFO  ]${NC} Starting the catalogue server"

tmux new-session -d -s cat "cd /home/ideam/cat-json-schema-server && tmux new-session -d 'npm start'"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Started catalogue server"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to start catalogue server"
fi

#!/bin/ash

RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'

rm -r /tmp/tmux-* > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Removed old tmux sessions"
else
    echo -e "${YELLOW}[  INFO  ]${NC} There are no tmux sessions to remove"
fi

if ! nc -z localhost 27017
then

echo -e "${YELLOW}[  INFO  ]${NC} Starting MongoDB"

tmux new-session -d -s mongo 'mongod'

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Started MongoDB"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to start MongoDB"
fi

else
echo -e "${YELLOW}[  INFO  ]${NC} MongoDB is running"
fi

if ! nc -z localhost 8000
then

echo -e "${YELLOW}[  INFO  ]${NC} Starting the catalogue server"

tmux new-session -d -s cat "cd /home/ideam/cat-json-schema-server && tmux new-session -d 'npm start'"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Started catalogue server"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to start catalogue server"
fi

else
echo -e "${YELLOW}[  INFO  ]${NC} Catalogue server is running"
fi
 

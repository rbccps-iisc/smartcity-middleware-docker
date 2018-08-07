#!/bin/ash

RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'

echo -e "${YELLOW}[  INFO  ]${NC} Starting Webserver"

nohup java -jar /usr/local/webserver/cdxapis.jar 2>/dev/null >/dev/null &

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Started Webserver"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to start Webserver"
fi

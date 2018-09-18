#!/bin/ash

RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'

if ! nc -z localhost 8080
then

echo -e "${YELLOW}[  INFO  ]${NC} Starting Webserver"

nohup java -jar /usr/local/webserver/cdxapis.jar 2>/var/log/cdxapis_error.log >/var/log/cdxapis_out.log &

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Started Webserver"
    echo -e "${YELLOW}[  INFO  ]${NC} Webserver Logs are at /var/log/"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to start Webserver"
fi

else
echo -e "${YELLOW}[  INFO  ]${NC} Webserver is running"
fi

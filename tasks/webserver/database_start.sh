#!/bin/ash

RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'


echo -e "${YELLOW}[  INFO  ]${NC} Starting Database Connector"

nohup java -jar /usr/local/webserver/cdxdatabase.jar 2>/var/log/cdxdatabase_error.log >/var/log/cdxdatabase_out.log &

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Started Database Connector"
    echo -e "${YELLOW}[  INFO  ]${NC} Database Connector Logs are at /var/log/"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to start Database Connector"
fi


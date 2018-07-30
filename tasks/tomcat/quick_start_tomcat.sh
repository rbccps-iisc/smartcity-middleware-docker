#!/bin/ash

RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'

if ! nc -z localhost 8080
then

echo -e "${YELLOW}[  INFO  ]${NC} Starting tomcat"

/usr/local/tomcat/bin/catalina.sh start > /dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Started Tomcat"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to start Tomcat"
fi

else
echo -e "${YELLOW}[  INFO  ]${NC} Tomcat is running"
fi

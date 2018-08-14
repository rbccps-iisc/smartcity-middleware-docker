#!/bin/ash

RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'


echo -e "${YELLOW}[  INFO  ]${NC} Creating Error Log File"

touch /var/log/cdxapis_error.log

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Created Error Log File"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to Create Error Log File"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Creating Out Log File"

touch /var/log/cdxapis_out.log

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Created Out Log File"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to Create Out Log File"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Changing Permission of Log File"

chmod +x /var/log/cdxapis_*

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Success Changing permission"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to change permission"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Starting Webserver"

nohup java -jar /usr/local/webserver/cdxapis.jar 2>/var/log/cdxapis_error.log >/var/log/cdxapis_out.log &

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Started Webserver"
    echo -e "${YELLOW}[   INFO   ]${NC} Webserver Logs are at /var/log/"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to start Webserver"
fi

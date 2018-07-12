#!/bin/ash

RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'

echo -e "${YELLOW}[  INFO  ]${NC} Copying CA user certificate keys"

echo "TrustedUserCAKeys /etc/ssh/ca-user-certificate-key.pub" >> /etc/ssh/sshd_config

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Copied CA user certificate keys"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to copy CA user certificate keys"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Starting tomcat"

/usr/local/tomcat/bin/catalina.sh start > /dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Started Tomcat"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to start Tomcat"
fi

#!/bin/bash

RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'

echo -e "${YELLOW}[  INFO  ]${NC} Copying RabbitMQ password file"

docker cp host_vars/rabbitmq rabbitmq:/etc/

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Copied password file"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to copy RabbitMQ password file"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Copying setup script into RabbitMQ container"

docker cp tasks/rabbitmq/install.sh rabbitmq:/etc/

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Copied setup script"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to copy setup script"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Adding necessary permissions to files and folders needed by RabbitMQ"

docker exec rabbitmq chmod +x /etc/install.sh

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Added permissions"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to add permissions to RabbitMQ files"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Starting setup script"

docker exec rabbitmq /etc/install.sh

echo -e "${YELLOW}[  INFO  ]${NC} Starting Go HTTP plugin"

docker exec rabbitmq /usr/local/go/bin/rabbitmq-http -address=0.0.0.0:8000 > /dev/null 2>&1 &

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Started HTTP plugin"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to start HTTP plugin"
fi

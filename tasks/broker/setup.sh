#!/bin/bash

RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'

echo -e "${YELLOW}[  INFO  ]${NC} Copying RabbitMQ password file"

docker cp host_vars/broker broker:/etc/

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Copied password file"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to copy RabbitMQ password file"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Copying RabbitMQ config file"

docker cp config/broker/rabbitmq.config broker:/etc/rabbitmq/

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Copied config file"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to copy RabbitMQ config file"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Copying setup script into RabbitMQ container"

docker cp tasks/broker/install.sh broker:/etc/

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Copied setup script"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to copy setup script"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Adding necessary permissions to files and folders needed by RabbitMQ"

docker exec broker chmod +x /etc/install.sh

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Added permissions"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to add permissions to RabbitMQ files"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Starting setup script"

docker exec broker /etc/install.sh

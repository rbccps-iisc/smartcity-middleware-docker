#!/bin/ash

RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'

if ! nc -z localhost 5672
then

echo -e "${YELLOW}[  INFO  ]${NC} Starting RabbitMQ in detached mode"

/home/ideam/rabbitmq_server-3.7.5/sbin/rabbitmq-server -detached 2>&1

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Started RabbitMQ server"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to start RabbitMQ server"
fi

else
echo -e "${YELLOW}[  INFO  ]${NC} RabbitMQ is running"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Waiting for RabbitMQ to start up"

while ! nc -z localhost 15672
do
sleep 0.1
done

echo -e "${GREEN}[   OK   ]${NC} RabbitMQ server is up"

if ! nc -z localhost 8000
then 

echo -e "${YELLOW}[  INFO  ]${NC} Starting Go HTTP plugin"

/usr/local/go/bin/rabbitmq-http -address=0.0.0.0:8000 > /dev/null 2>&1 &

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Started HTTP plugin"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to start HTTP plugin"
fi

else
echo -e "${YELLOW}[  INFO  ]${NC} Go plugin is running"
fi

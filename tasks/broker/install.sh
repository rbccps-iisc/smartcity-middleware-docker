#!/bin/ash

RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'

echo -e "${YELLOW}[  INFO  ]${NC} Deleting .erlang.cookie file"

find / -name ".erlang.cookie" | xargs rm

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Deleted cookie file" 
else
    echo -e "${RED}[ ERROR ]${NC} Failed to delete erlang cookie"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Starting RabbitMQ in detached mode"

rabbitmq-server -detached 2>&1

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Started RabbitMQ server"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to start RabbitMQ server"
fi

pwd=`cat /etc/broker | cut -d : -f 2 | awk '{$1=$1};1'`

echo -e "${YELLOW}[  INFO  ]${NC} Waiting for RabbitMQ to start up"

while ! nc -z localhost 15672
do
sleep 0.1
done

echo -e "${GREEN}[   OK   ]${NC} RabbitMQ server is up"

echo -e "${YELLOW}[  INFO  ]${NC} Creating admin.ideam user in RabbitMQ with administrator privileges"

curl -XPUT -u guest:guest "http://localhost:15672/api/users/admin.ideam" -d '{"password": "'"$pwd"'", "tags": "administrator", "permissions": { "/": { "configure": ".*","read": ".*","write":".*" } } }'

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Created admin.ideam user"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to create admin.ideam user"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Removing rabbitmq password file"

rm /etc/broker

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Deleted password file"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to delete password file"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Deleting guest user" 

rabbitmqctl delete_user guest > /dev/null 2>&1 

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Deleted guest user"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to delete guest user"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Restarting RabbitMQ"

rabbitmqctl stop_app > /dev/null 2>&1
rabbitmqctl start_app > /dev/null 2>&1

while ! nc -z localhost 15672
do
sleep 0.1
done

echo -e "${GREEN}[   OK   ]${NC} Restarted RabbitMQ" 

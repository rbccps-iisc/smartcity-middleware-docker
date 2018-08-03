#!/bin/ash

RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'

#echo -e "${YELLOW}[  INFO  ]${NC} Copying CA user certificate keys"

#echo "TrustedUserCAKeys /etc/ssh/ca-user-certificate-key.pub" >> /etc/ssh/sshd_config

#if [ $? -eq 0 ]; then
#    echo -e "${GREEN}[   OK   ]${NC} Copied CA user certificate keys"
#else
#    echo -e "${RED}[ ERROR ]${NC} Failed to copy CA user certificate keys"
#fi

echo -e "${YELLOW}[  INFO  ]${NC} Starting RabbitMQ in detached mode"

/home/ideam/rabbitmq_server-3.7.5/sbin/rabbitmq-server -detached 2>&1

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Started RabbitMQ server"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to start RabbitMQ server"
fi

pwd=`cat /etc/rabbitmq | cut -d : -f 2 | awk '{$1=$1};1'`

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

rm /etc/rabbitmq

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Deleted password file"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to delete password file"
fi

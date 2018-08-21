#!/bin/ash

RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'

pwd=`cat /etc/rabbitmq | cut -d : -f 2 | awk '{$1=$1};1'`

echo -e "${YELLOW}[  INFO  ]${NC} Changing passwords in files"

sed -i 's/rmq_user/admin.ideam/g' /home/ideam/logstash-6.2.4/config/logstash-input-rabbitmq.conf
sed -i 's/rmq_pwd/'$pwd'/g' /home/ideam/logstash-6.2.4/config/logstash-input-rabbitmq.conf

echo -e "${GREEN}[   OK   ]${NC} Changed passwords"

echo -e "${YELLOW}[  INFO  ]${NC} Removing RabbitMQ password file"

rm /etc/rabbitmq

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Removed password file"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to remove password file"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Starting Elasticsearch"

tmux new-session -d -s elasticsearch 'su ideam -c "/home/ideam/elasticsearch-6.2.4/bin/elasticsearch"'

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Started Elasticsearch"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to start elastcisearch"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Starting Logstash"

tmux new-session -d -s logstash '/home/ideam/logstash-6.2.4/bin/logstash -f /home/ideam/logstash-6.2.4/config/logstash-input-rabbitmq.conf'

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Started Logstash"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to start Logstash"
fi

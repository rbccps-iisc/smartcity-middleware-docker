#!/bin/ash

RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'

rm -r /tmp/tmux-*

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Removed old tmux sessions"
else
    echo -e "${YELLOW}[  INFO  ]${NC} There are no tmux sessions to remove"
fi

if ! nc -z localhost 9200
then

echo -e "${YELLOW}[  INFO  ]${NC} Starting Elasticsearch"

tmux new-session -d -s elasticsearch 'su ideam -c "/home/ideam/elasticsearch-6.2.4/bin/elasticsearch"'

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Started Elasticsearch"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to start elastcisearch"
fi

else
echo -e "${YELLOW}[  INFO  ]${NC} Elasticsearch is running"
fi

if nc -z localhost 9600
then
 
echo -e "${YELLOW}[  INFO  ]${NC} Starting Logstash"

tmux new-session -d -s logstash '/home/ideam/logstash-6.2.4/bin/logstash -f /home/ideam/logstash-6.2.4/config/logstash-input-rabbitmq.conf'

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Started Logstash"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to start Logstash"
fi

else
echo -e "${YELLOW}[  INFO  ]${NC} Logstash is running"
fi

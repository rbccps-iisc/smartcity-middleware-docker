#!/bin/ash

RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'

echo -e "${YELLOW}[  INFO  ]${NC} Starting Elasticsearch"

tmux new-session -d -s elasticsearch 'su ideam -c "/home/ideam/elasticsearch-6.2.4/bin/elasticsearch"'

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Started Elasticsearch"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to start elastcisearch"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Starting Kibana"

tmux new-session -d -s kibana '/home/ideam/kibana-6.2.4-linux-x86_64/bin/kibana'

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Started Kibana"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to start Kibana"
fi

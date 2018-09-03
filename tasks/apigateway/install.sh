#!/bin/ash

RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'

echo -e "${YELLOW}[  INFO  ]${NC} Starting postgres"

su postgres -c "postgres -D /var/lib/postgresql > /var/lib/postgresql/logfile 2>&1 &"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Started Postgres"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to start postgres. Check /var/lib/postgresql/logfile for more details"
fi

#TODO set a timeout

echo -e "${YELLOW}[  INFO  ]${NC} Waiting for the database system to start up"

until su postgres -c 'pg_isready' >/dev/null 2>&1
do
  sleep 0.1
done

echo -e "${GREEN}[   OK   ]${NC} Postgres is ready"

echo -e "${YELLOW}[  INFO  ]${NC} Starting Kong"

kong start -c /etc/kong/kong.conf > /dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Started Kong"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to start Kong. Check /usr/local/kong/logs/error.log for more details"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Applyling API configurations"

kongfig apply --path /etc/config.yml --host localhost:8001

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Applied API configurations"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to apply API configurations"
fi


#!/bin/ash

RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'

rm -r /tmp/tmux-* > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Removed old tmux sessions"
else
    echo -e "${YELLOW}[  INFO  ]${NC} There are no tmux sessions to remove"
fi

rm /var/lib/postgresql/postmaster.* > /dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Removed old postmaster files"
else
    echo -e "${YELLOW}[  INFO  ]${NC} There are no postmaster files to remove"
fi

rm /tmp/.s.PGSQL.5432 > /dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Removed PGSQL file"
else
    echo -e "${YELLOW}[  INFO  ]${NC} There is no PGSQL file to remove"
fi

rm /tmp/.s.PGSQL.5432.lock > /dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Removed PGSQL lock file"
else
    echo -e "${YELLOW}[  INFO  ]${NC} There is no PGSQL lock file to remove"
fi

if ! nc -z localhost 5432
then
echo -e "${YELLOW}[  INFO  ]${NC} Starting postgres"

su postgres -c "postgres -D /var/lib/postgresql  > /var/lib/postgresql/logfile 2>&1 &"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Started Postgres"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to start postgres. Check /var/lib/postgresql/logfile for more details"
fi

else

echo -e "${YELLOW}[  INFO  ]${NC} Postgres is already running"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Waiting for the database system to start up"

until su postgres -c 'pg_isready' > /dev/null 2>&1
do
  sleep 0.1
done

echo -e "${GREEN}[   OK   ]${NC} Postgres is ready"

if ! nc -z localhost 8000
then
echo -e "${YELLOW}[  INFO  ]${NC} Starting Kong"

kong start -c /etc/kong/kong.conf > /dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Started Kong"
else
    echo -e "${RED}[ ERROR ]${NC} Failed to start Kong. Check /usr/local/kong/logs/error.log for more details"
fi

else
echo -e "${YELLOW}[  INFO  ]${NC} Kong is running"
fi

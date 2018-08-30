#!/bin/ash

RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'

echo -e "${YELLOW}[  INFO  ]${NC} Setting up database subscriber log files"

touch /usr/local/kong/database_error.log
touch /usr/local/kong/database_out.log

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC}Log Setup Completed"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to create log files"
fi

#!/bin/ash

RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'

echo -e "${YELLOW}[  INFO  ]${NC} Starting NGINX"

/usr/local/nginx/sbin/nginx

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC}Started NGINX"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to start NGINX"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Starting PHP FPM"

/usr/sbin/php-fpm7

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC}Started PHP-FPM"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to start PHP-FPM"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Starting backend server"
tmux new-session -d -s my_session 'npm start --prefix /usr/local/nginx/html/Video-server-backend/'

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ] ${NC}Started backend server"
else
    echo -e "${RED}[ ERROR ] ${NC}Failed to start backend server"
fi

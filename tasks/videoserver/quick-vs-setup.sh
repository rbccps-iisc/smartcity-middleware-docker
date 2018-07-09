#!/bin/ash

echo -e "\nStarting NGINX"
/usr/local/nginx/sbin/nginx

echo -e "\nStarting PHP FPM"
/usr/sbin/php-fpm7

echo -e "\nStarting backend server"
tmux new-session -d -s my_session 'npm start --prefix /usr/local/nginx/html/Video-server-backend/'

#!/bin/bash

echo -e "\nCopying CA user certificate key"
docker cp config/certificate_authority/keys/ca-user-certificate-key.pub rabbitmq:/etc/ssh/ca-user-certificate-key.pub
docker exec -i rabbitmq mkdir -p /root/.ssh/ 

echo -e "\nAdding user's SSH public key into authorised keys"
docker exec -i rabbitmq dd of=/root/.ssh/authorized_keys < ~/.ssh/id_rsa.pub > /dev/null 2>&1

echo -e "\nCopying RabbitMQ config file"
docker cp config/rabbitmq/rabbitmq.config rabbitmq:/home/ideam/rabbitmq_server-3.7.5/etc/rabbitmq
docker cp host_vars/rabbitmq rabbitmq:/etc/

echo -e "\nCopying setup script into RabbitMQ container"
docker cp tasks/rabbitmq/quick-rmq-setup.sh rabbitmq:/etc/

echo -e "\nAdding necessary permissions to files and folders needed by RabbitMQ"
docker exec rabbitmq chmod +x /etc/quick-rmq-setup.sh

echo -e "\nStarting setup script"
docker exec rabbitmq /etc/quick-rmq-setup.sh 

echo -e "\nStarting Go HTTP plugin"
docker exec rabbitmq /usr/local/go/bin/rabbitmq-http -address=0.0.0.0:8000 > /dev/null 2>&1 &

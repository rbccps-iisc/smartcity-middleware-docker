#!/bin/bash

echo -e "\nCopying CA user certifiate key"
docker cp config/certificate_authority/keys/ca-user-certificate-key.pub elasticsearch:/etc/ssh/ca-user-certificate-key.pub
docker exec -i elasticsearch mkdir -p /root/.ssh/ 

echo -e "\nAdding user's SSH public key into authorised keys"
docker exec -i elasticsearch dd of=/root/.ssh/authorized_keys < ~/.ssh/id_rsa.pub > /dev/null 2>&1

echo -e "\nCopying RabbitMQ password"
docker cp host_vars/rabbitmq elasticsearch:/etc/

echo -e "\nCopying setup script into elasticsearch container"
docker cp tasks/elasticsearch/quick-elk-setup.sh elasticsearch:/etc/

echo -e "\nAdding necessary permissions to files and folders needed by elasticsearch"
docker exec elasticsearch chmod +x /etc/quick-elk-setup.sh 

echo -e "\nStarting setup script"
docker exec elasticsearch /etc/quick-elk-setup.sh

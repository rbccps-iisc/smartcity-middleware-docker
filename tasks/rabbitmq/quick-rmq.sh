#!/bin/bash
docker cp config/certificate_authority/keys/ca-user-certificate-key.pub rabbitmq:/etc/ssh/ca-user-certificate-key.pub
docker exec -i rabbitmq mkdir -p /root/.ssh/ 
docker exec -i rabbitmq dd of=/root/.ssh/authorized_keys < ~/.ssh/id_rsa.pub
docker cp config/rabbitmq/rabbitmq.config rabbitmq:/home/ideam/rabbitmq_server-3.7.5/etc/rabbitmq
docker cp host_vars/rabbitmq rabbitmq:/etc/
sshpass -p "rbccps@123456" ssh root@localhost -p $1 < tasks/rabbitmq/quick-rmq-setup.sh 

#!/bin/bash
docker cp config/certificate_authority/keys/ca-user-certificate-key.pub elasticsearch:/etc/ssh/ca-user-certificate-key.pub
docker exec -i elasticsearch mkdir -p /root/.ssh/ 
docker exec -i elasticsearch dd of=/root/.ssh/authorized_keys < ~/.ssh/id_rsa.pub > /dev/null 2>&1
docker cp host_vars/rabbitmq elasticsearch:/etc/
#sshpass -p "rbccps@123456" ssh root@localhost -p $1 < tasks/elasticsearch/quick-elk-setup.sh 
docker cp tasks/elasticsearch/quick-elk-setup.sh elasticsearch:/etc/
docker exec elasticsearch chmod +x /etc/quick-elk-setup.sh 
docker exec elasticsearch /etc/quick-elk-setup.sh

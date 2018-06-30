#!/bin/bash
docker cp config/certificate_authority/keys/ca-user-certificate-key.pub kong:/etc/ssh/ca-user-certificate-key.pub
docker exec -i kong mkdir -p /root/.ssh/ 
docker exec -i kong dd of=/root/.ssh/authorized_keys < ~/.ssh/id_rsa.pub > /dev/null 2>&1
docker cp host_vars/rabbitmq kong:/etc
docker cp host_vars/ldapd kong:/etc
#sshpass -p "rbccps@123456" ssh root@localhost -p $1 < tasks/kong/quick-kong-setup.sh 
docker cp tasks/kong/quick-kong-setup.sh kong:/etc/
docker exec kong chmod 777 /etc/quick-kong-setup.sh
docker exec kong chmod -R 777 /var/lib/postgresql 
docker exec kong /etc/quick-kong-setup.sh

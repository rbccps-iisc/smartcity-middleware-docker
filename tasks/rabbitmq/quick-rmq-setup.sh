#!/bin/ash

echo -e "\nCopying CA user certificate keys"
echo "TrustedUserCAKeys /etc/ssh/ca-user-certificate-key.pub" >> /etc/ssh/sshd_config

echo -e "\nStarting RabbitMQ in detached mode"
/home/ideam/rabbitmq_server-3.7.5/sbin/rabbitmq-server -detached
pwd=`cat /etc/rabbitmq | cut -d : -f 2 | awk '{$1=$1};1'`

echo -e "\nWaiting for RabbitMQ to start up"
while ! nc -z localhost 15672
do
sleep 0.1
done

echo -e "\nCreating admin.ideam user"
curl -XPUT -u guest:guest "http://localhost:15672/api/users/admin.ideam" -d '{"password": "'"$pwd"'", "tags": "administrator", "permissions": { "/": { "configure": ".*","read": ".*","write":".*" } } }'

rm /etc/rabbitmq

#supervisord -c /etc/supervisord.conf
#supervisorctl start all

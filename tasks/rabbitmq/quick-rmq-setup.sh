#!/bin/ash
echo "TrustedUserCAKeys /etc/ssh/ca-user-certificate-key.pub" >> /etc/ssh/sshd_config
/home/ideam/rabbitmq_server-3.7.5/sbin/rabbitmq-server -detached
#echo -e "\e[31;43m***** STARTING GO PLUGIN *****\e[0m"
pwd=`cat /etc/rabbitmq | cut -d : -f 2 | awk '{$1=$1};1'`

while ! nc -z localhost 15672
do
sleep 0.1
done

curl -XPUT -u guest:guest "http://localhost:15672/api/users/admin.ideam" -d '{"password": "'"$pwd"'", "tags": "administrator", "permissions": { "/": { "configure": ".*","read": ".*","write":".*" } } }'

rm /etc/rabbitmq

#supervisord -c /etc/supervisord.conf
#supervisorctl start all

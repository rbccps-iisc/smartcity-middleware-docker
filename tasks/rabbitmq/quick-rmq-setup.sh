#!/bin/ash
echo "TrustedUserCAKeys /etc/ssh/ca-user-certificate-key.pub" >> /etc/ssh/sshd_config
apk add --update --no-cache tmux curl
/home/ideam/rabbitmq_server-3.7.5/sbin/rabbitmq-server -detached
tmux new-session -d -s my_session 'rabbitmq-http -address=0.0.0.0:8000'
pwd=`cat /etc/rabbitmq | cut -d : -f 2 | awk '{$1=$1};1'`
sleep 5
curl -XPUT -u guest:guest "http://localhost:15672/api/users/admin.ideam" -d '{"password": "'"$pwd"'", "tags": "administrator", "permissions": { "/": { "configure": ".*","read": ".*","write":".*" } } }'
rm /etc/rabbitmq

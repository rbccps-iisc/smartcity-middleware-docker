#!/bin/ash
echo "TrustedUserCAKeys /etc/ssh/ca-user-certificate-key.pub" >> /etc/ssh/sshd_config
pwd=`cat /etc/rabbitmq | cut -d : -f 2 | awk '{$1=$1};1'`
sed -i 's/rmq_user/admin.ideam/g' /home/ideam/logstash-6.2.4/config/logstash-input-rabbitmq.conf
sed -i 's/rmq_pwd/'$pwd'/g' /home/ideam/logstash-6.2.4/config/logstash-input-rabbitmq.conf
rm /etc/rabbitmq
tmux new-session -d -s elasticsearch 'su ideam -c "/home/ideam/elasticsearch-6.2.4/bin/elasticsearch"'
sleep 10
tmux new-session -d -s logstash '/home/ideam/logstash-6.2.4/bin/logstash -f /home/ideam/logstash-6.2.4/config/logstash-input-rabbitmq.conf'

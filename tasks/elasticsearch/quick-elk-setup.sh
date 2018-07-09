#!/bin/ash

echo -e "\nCopying CA user certificate keys"
echo "TrustedUserCAKeys /etc/ssh/ca-user-certificate-key.pub" >> /etc/ssh/sshd_config
pwd=`cat /etc/rabbitmq | cut -d : -f 2 | awk '{$1=$1};1'`

echo -e "\nChanging passwords in files"
sed -i 's/rmq_user/admin.ideam/g' /home/ideam/logstash-6.2.4/config/logstash-input-rabbitmq.conf
sed -i 's/rmq_pwd/'$pwd'/g' /home/ideam/logstash-6.2.4/config/logstash-input-rabbitmq.conf
rm /etc/rabbitmq

echo -e "\nStarting Elasticsearch"
tmux new-session -d -s elasticsearch 'su ideam -c "/home/ideam/elasticsearch-6.2.4/bin/elasticsearch"'

#while ! nc -z localhost 9200
#do
#sleep 0.1
#done

echo -e "\nStarting Logstash"
tmux new-session -d -s logstash '/home/ideam/logstash-6.2.4/bin/logstash -f /home/ideam/logstash-6.2.4/config/logstash-input-rabbitmq.conf'

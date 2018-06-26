#!/bin/ash
echo "TrustedUserCAKeys /etc/ssh/ca-user-certificate-key.pub" >> /etc/ssh/sshd_config
su postgres -c "/usr/local/pgsql/bin/postgres -D /usr/local/pgsql/data >/var/lib/postgresql/logfile 2>&1 &"
sleep 5
kong start -c /etc/kong/kong.conf
sleep 5
rmqpwd=`cat /etc/rabbitmq | cut -d : -f 2 | awk '{$1=$1};1'`
ldapdpwd=`cat /etc/ldapd | cut -d : -f 2 | awk '{$1=$1};1'`
sed -i 's/rmq_user/admin.ideam/g' /home/ideam/share.py
sed -i 's/rmq_pwd/'$rmqpwd'/g' /home/ideam/share.py
sed -i 's/ldap_pwd/'$ldapdpwd'/g' /home/ideam/share.py
tmux new-session -d -s share 'python3.6 /home/ideam/share.py'

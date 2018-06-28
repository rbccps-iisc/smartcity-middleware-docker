#!/bin/ash
echo "TrustedUserCAKeys /etc/ssh/ca-user-certificate-key.pub" >> /etc/ssh/sshd_config
pwd=`cat /etc/ldapd | cut -d : -f 2 | awk '{$1=$1};1'`
sed -i 's/ldap_pwd/'$pwd'/g' /home/ideam/cat-json-schema-server/lib/config.js
rm /etc/ldapd
tmux new-session -d -s mongo 'mongod'

while ! nc -z localhost 27017
do
sleep 0.1
done

tmux new-session -d -s cat "cd /home/ideam/cat-json-schema-server && tmux new-session -d 'npm start'"

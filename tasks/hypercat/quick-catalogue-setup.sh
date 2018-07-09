#!/bin/ash

echo -e "\nCopying CA user certificate keys"
echo "TrustedUserCAKeys /etc/ssh/ca-user-certificate-key.pub" >> /etc/ssh/sshd_config
pwd=`cat /etc/ldapd | cut -d : -f 2 | awk '{$1=$1};1'`

echo -e "\nChanging passwords in files"
sed -i 's/ldap_pwd/'$pwd'/g' /home/ideam/cat-json-schema-server/lib/config.js
rm /etc/ldapd

echo -e "\nStarting MongoDB"
tmux new-session -d -s mongo 'mongod'

echo -e "\nWaiting for MongoDB to start up"
while ! nc -z localhost 27017
do
sleep 0.1
done

echo -e "\nStarting the catalogue server"
tmux new-session -d -s cat "cd /home/ideam/cat-json-schema-server && tmux new-session -d 'npm start'"

#!/bin/ash

echo -e "\nCopy CA user certificate keys"
echo "TrustedUserCAKeys /etc/ssh/ca-user-certificate-key.pub" >> /etc/ssh/sshd_config
pwd=`cat /etc/ldapd | cut -d : -f 2 | awk '{$1=$1};1'`

echo -e "\nChanging passwords in files"
sed -i 's/ldap_pwd/'$pwd'/g' /etc/ldapd.conf

echo -e "\nStarting LDAP"
/usr/local/sbin/ldapd

echo -e "\nWaiting for LDAP to start up"
while ! nc -z localhost 8389
do
sleep 0.1
done

echo -e "\nAdding LDIF files"
ldapmodify -h 127.0.0.1 -p 8389 -x -D cn=admin,dc=smartcity -w $pwd -f /smartcity.ldif
ldapmodify -h 127.0.0.1 -p 8389 -x -D cn=admin,dc=smartcity -w $pwd -f /devices.ldif
rm /etc/ldapd

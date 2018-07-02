#!/bin/ash
echo "TrustedUserCAKeys /etc/ssh/ca-user-certificate-key.pub" >> /etc/ssh/sshd_config
pwd=`cat /etc/ldapd | cut -d : -f 2 | awk '{$1=$1};1'`
sed -i 's/ldap_pwd/'$pwd'/g' /etc/ldapd.conf
/usr/local/sbin/ldapd

while ! nc -z localhost 8389
do
sleep 0.1
done

ldapmodify -h 127.0.0.1 -p 8389 -x -D cn=admin,dc=smartcity -w $pwd -f /smartcity.ldif
ldapmodify -h 127.0.0.1 -p 8389 -x -D cn=admin,dc=smartcity -w $pwd -f /devices.ldif
rm /etc/ldapd

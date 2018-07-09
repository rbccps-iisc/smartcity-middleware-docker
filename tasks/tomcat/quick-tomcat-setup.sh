#!/bin/ash

echo -e "\nCopying CA user certificate keys"
echo "TrustedUserCAKeys /etc/ssh/ca-user-certificate-key.pub" >> /etc/ssh/sshd_config

echo -e "\nStarting tomcat"
/usr/local/tomcat/bin/catalina.sh start

#!/bin/ash

while :
do
ldapd -dvvv
ldapctl compact
ldapctl index
echo "restarted" >> file 
done


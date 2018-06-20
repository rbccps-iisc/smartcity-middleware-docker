#!/bin/ash
ssh-keygen -t rsa -b 2048 -f .ssh/ca-user-certificate-key
ssh-keygen -s /root/.ssh/ca-user-certificate-key -I user_ansible -n ideam,root /root/id_rsa.pub

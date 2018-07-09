#!/bin/bash

echo -e "\nCopying CA user certifiate key"
docker cp config/certificate_authority/keys/ca-user-certificate-key.pub videoserver:/etc/ssh/ca-user-certificate-key.pub
docker exec videoserver mkdir -p /root/.ssh/

echo -e "\nAdding user's SSH public key into authorised keys"
docker exec videoserver dd of=/root/.ssh/authorized_keys < ~/.ssh/id_rsa.pub > /dev/null 2>&1

echo -e "\nCopying setup script"
docker cp tasks/videoserver/quick-vs-setup.sh videoserver:/etc/

echo -e "\nAdding necessary permissions to files and folders needed by videoserver"
docker exec videoserver chmod 777 /etc/quick-vs-setup.sh

echo -e "\nStarting setup script"
docker exec videoserver /etc/quick-vs-setup.sh

#!/bin/bash
docker cp config/certificate_authority/keys/id_rsa.pub certificate_authority:/root/
ssh -o "StrictHostKeyChecking=no" root@localhost -p $1 < tasks/certificate_authority/sign.sh
docker cp certificate_authority:/root/id_rsa-cert.pub config/certificate_authority/keys
docker cp certificate_authority:/root/.ssh/ca-user-certificate-key.pub config/certificate_authority/keys/ 
docker cp certificate_authority:/root/id_rsa-cert.pub ~/.ssh/

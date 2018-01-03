#!/usr/bin/env bash
sudo apt-get update && sudo apt-get install software-properties-common && sudo apt-add-repository ppa:ansible/ansible && sudo apt-get update && sudo apt-get install -y ansible
sudo apt-get install -y apt-transport-https  ca-certificates curl software-properties-common
git clone https://github.com/rbccps-iisc/smartcity-middleware-docker.git
apt install python-pip python
python -m pip install pathlib2
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-get update
apt-get install docker-ce
mkdir -p /data/kong
mkdir -p /data/kong-config
mkdir -p /data/catalogue
mkdir -p /data/rabbitmq
mkdir -p /data/ldap
ssh-keygen
chmod 777 /data/*
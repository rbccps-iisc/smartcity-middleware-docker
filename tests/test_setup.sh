#!/usr/bin/env bash
sudo apt-get update && sudo apt-get install -y software-properties-common && sudo apt-add-repository ppa:ansible/ansible && sudo apt-get update && sudo apt-get install -y ansible
sudo apt-get install -y apt-transport-https  ca-certificates curl software-properties-common
git clone https://github.com/rbccps-iisc/smartcity-middleware-docker.git
apt install python-pip python -y
python -m pip install pathlib2
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-get update
apt-get install docker-ce -y
mkdir -p /data/kong
mkdir -p /data/kong-config
mkdir -p /data/catalogue
mkdir -p /data/rabbitmq
mkdir -p /data/ldap
ssh-keygen
chmod 777 /data/*
dd if=/dev/zero of=/swapfile bs=1024 count=2048k
mkswap /swapfile
swapon /swapfile
echo 10 | sudo tee /proc/sys/vm/swappiness
echo vm.swappiness = 10 | sudo tee -a /etc/sysctl.conf
chown root:root /swapfile
chmod 0600 /swapfile
#!/usr/bin/env bash
sudo apt-get -y update && sudo apt-get install -y software-properties-common && sudo apt-add-repository ppa:ansible/ansible -y && sudo apt-get -y update && sudo apt-get install -y ansible
sudo apt-get install -y apt-transport-https  ca-certificates curl software-properties-common
sudo apt install python-pip python -y
python -m pip install pathlib2
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" -y
sudo apt-get update -y
sudo apt-get install docker-ce -y
sudo mkdir -p /data/kong
sudo mkdir -p /data/kong-config
sudo mkdir -p /data/catalogue
sudo mkdir -p /data/rabbitmq
sudo mkdir -p /data/ldap
sudo mkdir -p /data/tomcat
sudo mkdir -p /data/logs/kong
sudo mkdir -p /data/logs/rabbitmq
sudo mkdir -p /data/logs/tomcat
sudo usermod -aG docker $USER
ssh-keygen -f $HOME/.ssh/id_rsa -t rsa -N ''
sudo chmod -R 777 /data/*
sudo sysctl -w vm.max_map_count=662144

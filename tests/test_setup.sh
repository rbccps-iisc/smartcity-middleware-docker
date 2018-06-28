#!/usr/bin/env bash
# The following are the packages to be installed in a new vm machine for test purposes.
# Ansible, docker and python.
sudo apt-get -y update && sudo apt-get install -y software-properties-common && sudo apt-add-repository ppa:ansible/ansible -y && sudo apt-get -y update && sudo apt-get install -y ansible
sudo apt-get install -y apt-transport-https  ca-certificates curl software-properties-common
sudo apt install python python-pip -y
python -m pip install passlib
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" -y
sudo apt-get update -y
sudo apt-get install docker-ce -y
sudo usermod -aG docker $USER
# create ssh keys
ssh-keygen -f $HOME/.ssh/id_rsa -t rsa -N ''
# vm.max_map_count must be set to higher value for elasticsearch.
sudo sysctl -w vm.max_map_count=662144
sudo apt-get install sshpass

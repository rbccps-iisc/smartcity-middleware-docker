#!/usr/bin/env bash
cd build/
mkdir ideam_0.0-1
mkdir -p ideam_0.0-1/usr/local/bin
mkdir -p ideam_0.0-1/usr/share/ideam
mkdir -p ideam_0.0-1/etc/ideam
mkdir -p ideam_0.0-1/DEBIAN
mkdir -p ideam_0.0-1/var/ideam/data/kong
mkdir -p ideam_0.0-1/var/ideam/data/kong-config
mkdir -p ideam_0.0-1/var/ideam/data/catalogue
mkdir -p ideam_0.0-1/var/ideam/data/rabbitmq
mkdir -p ideam_0.0-1/var/ideam/data/ldap
mkdir -p ideam_0.0-1/var/ideam/data/tomcat
mkdir -p ideam_0.0-1/var/ideam/data/logs/kong
mkdir -p ideam_0.0-1/var/ideam/data/logs/rabbitmq
mkdir -p ideam_0.0-1/var/ideam/data/logs/tomcat
cp ../ideam.py ideam_0.0-1/usr/local/bin/ideam
cp debian/control ideam_0.0-1/DEBIAN/control
cp ../middleware.conf ideam_0.0-1/etc/ideam/
chmod +x ideam_0.0-1/usr/local/bin/ideam
cd ../
tar --exclude='./build' --exclude='./.git' --exclude='./.idea' --exclude='*.retry' --exclude='*.tar.gz' --exclude='./ideam.tgz' --exclude='*.DS_Store' --exclude='./.gitignore' -zcvf ideam.tgz ./
tar -xvzf ideam.tgz -C build/ideam_0.0-1/usr/share/ideam/
cd build/
sudo dpkg-deb --build ideam_0.0-1/
sudo dpkg -i ideam_0.0-1.deb
sudo dpkg --remove ideam
sudo apt-get -y update && sudo apt-get install -y software-properties-common && sudo apt-add-repository ppa:ansible/ansible -y && sudo apt-get -y update && sudo apt-get install -y ansible
sudo apt-get install -y apt-transport-https  ca-certificates curl software-properties-common
sudo apt install python-pip python -y
python -m pip install pathlib2
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" -y
sudo apt-get update -y
sudo apt-get install docker-ce -y
sudo usermod -aG docker $USER
ssh-keygen -f $HOME/.ssh/id_rsa -t rsa -N ''
sudo sysctl -w vm.max_map_count=662144
sudo dpkg -i ideam_0.0-1.deb

#!/usr/bin/env bash
cd ./build/
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
cp ../ideam.conf ideam_0.0-1/etc/ideam/
chmod +x ideam_0.0-1/usr/local/bin/ideam
cd ../
tar --exclude='./build' --exclude='./.git' --exclude='./.idea' --exclude='*.retry' --exclude='*.tar.gz' --exclude='./ideam.tgz' --exclude='*.DS_Store' --exclude='./.gitignore' -zcvf ideam.tgz ./
tar -xvzf ideam.tgz -C build/ideam_0.0-1/usr/share/ideam/
cd build/
chmod -R 777 ideam_0.0-1/var/ideam/data/logs/kong
dpkg-deb --build ideam_0.0-1/
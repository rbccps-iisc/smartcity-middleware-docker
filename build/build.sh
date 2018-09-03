#!/usr/bin/env bash
cd ./build/
mkdir ideam_0.0-1
mkdir -p ideam_0.0-1/usr/local/bin
mkdir -p ideam_0.0-1/usr/share/ideam
mkdir -p ideam_0.0-1/etc/ideam
mkdir -p ideam_0.0-1/DEBIAN
mkdir -p ideam_0.0-1/var/ideam/data/apigateway
mkdir -p ideam_0.0-1/var/ideam/data/apigateway-config
mkdir -p ideam_0.0-1/var/ideam/data/catalogue
mkdir -p ideam_0.0-1/var/ideam/data/broker
mkdir -p ideam_0.0-1/var/ideam/data/ldap
mkdir -p ideam_0.0-1/var/ideam/data/webserver
mkdir -p ideam_0.0-1/var/ideam/data/logs/apigateway
mkdir -p ideam_0.0-1/var/ideam/data/logs/broker
mkdir -p ideam_0.0-1/var/ideam/data/logs/webserver
cp ../ideam.py ideam_0.0-1/usr/local/bin/ideam
cp debian/control ideam_0.0-1/DEBIAN/control
cp debian/prerm ideam_0.0-1/DEBIAN/prerm
chmod 755 ideam_0.0-1/DEBIAN/prerm
cp ../ideam.conf ideam_0.0-1/etc/ideam/
chmod +x ideam_0.0-1/usr/local/bin/ideam
cd ../
tar --exclude='./build' --exclude='./.git' --exclude='./.idea' --exclude='*.retry' --exclude='*.tar.gz' --exclude='./ideam.tgz' --exclude='*.DS_Store' --exclude='./.gitignore' -zcvf ideam.tgz ./
tar -xvzf ideam.tgz -C build/ideam_0.0-1/usr/share/ideam/
rm ideam.tgz
cd build/
chmod -R 777 ideam_0.0-1/var/ideam/data/logs/apigateway
dpkg-deb --build ideam_0.0-1/

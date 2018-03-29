#!/usr/bin/env bash

sudo apt-get install sshpass
sshpass -p $1 ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no ansible@localhost -p 10022
uname -a

#!/usr/bin/env bash
sshpass -p $1 ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no ansible@localhost -p 14022
uname -a

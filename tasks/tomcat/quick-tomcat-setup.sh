#!/bin/ash
apk add --update --no-cache tmux
echo "TrustedUserCAKeys /etc/ssh/ca-user-certificate-key.pub" >> /etc/ssh/sshd_config
tmux new-session -d -s my_session '/usr/local/tomcat/bin/catalina.sh run'

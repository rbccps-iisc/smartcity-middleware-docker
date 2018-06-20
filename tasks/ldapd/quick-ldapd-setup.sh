echo "TrustedUserCAKeys /etc/ssh/ca-user-certificate-key.pub" >> /etc/ssh/sshd_config
apk add --update --no-cache tmux
tmux new-session -d -s my_session '/usr/local/sbin/ldapd'

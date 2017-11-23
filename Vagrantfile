Vagrant.configure("2") do |config|
  config.vm.box = "tvlooy/openbsd-6.2-amd64"
  config.vm.box_version = "6.2.0"
  config.vm.hostname = "ldapd"
  config.vm.network "forwarded_port", guest: 389, host: 8389
  config.vm.provider "virtualbox" do |v|
    v.memory = 1024
    v.cpus = 1
  end
  config.vm.provision "file", source: "config/certificate_authority/keys/ca-user-certificate-key.pub", destination: "/home/vagrant/ca-user-certificate-key.pub"
  config.vm.provision "file", source: "config/ldapd/ldapd.conf", destination: "/home/vagrant/ldapd.conf"
  config.vm.provision "file", source: "config/ldapd/smartcity.ldif", destination: "/home/vagrant/smartcity.ldif"
  config.vm.provision "file", source: "config/ldapd/devices.ldif", destination: "/home/vagrant/devices.ldif"
  config.vm.provision "shell" do |s|
      s.inline = <<-SHELL
      cat /home/vagrant/ca-user-certificate-key.pub >> /etc/ssh/ca-user-certificate-key.pub
      sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config
      echo "TrustedUserCAKeys /etc/ssh/ca-user-certificate-key.pub" >> /etc/ssh/sshd_config
    SHELL
  end
  config.vm.provision :shell, privileged: false, inline: "sudo rcctl restart sshd"
  config.vm.provision :shell, privileged: false, inline: "sudo pkg_add openldap-client-2.4.45p4"
  config.vm.provision :shell, privileged: false, inline: "sudo cp /home/vagrant/ldapd.conf /etc/ldapd.conf"
  config.vm.provision :shell, privileged: false, inline: "sudo chmod 640 /etc/ldapd.conf"
  config.vm.provision 'deploy', type: :shell, privileged: false, inline: "sudo ldapd"
  config.vm.provision :shell, privileged: false, inline: "ldapmodify -h 127.0.0.1 -p 389 -x -D cn=admin,dc=smartcity -w secret0 -f smartcity.ldif"
  config.vm.provision :shell, privileged: false, inline: "ldapmodify -h 127.0.0.1 -p 389 -x -D cn=admin,dc=smartcity -w secret0 -f devices.ldif"
end
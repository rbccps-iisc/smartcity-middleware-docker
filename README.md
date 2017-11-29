# Smart City Middleware using Docker


### Web Page:
[https://rbccps.org/smartcity/](https://rbccps.org/smartcity/doku.php)

### Architecture:

![alt text](http://rbccps.org/smartcity/lib/exe/fetch.php?cache=&media=middleware_architecture.png)

### Requirements:
  * `Docker`: [Installation steps for Docker in Ubuntu/Debian](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#os-requirements)
  * `Vagrant`: [Installation steps for Vagrant in Ubuntu/Debian](https://www.vagrantup.com/downloads.html)
  * `VirtualBox`: [Installation steps for VirtualBox in Ubuntu/Debian](https://www.virtualbox.org/wiki/Linux_Downloads)
  * `Ansible`: [Installation steps for Ansible](http://docs.ansible.com/ansible/latest/intro_installation.html)
  * `Python-pip`: Installation dependency on Pathlib2. Use the command `python -m pip install pathlib2`

### Release:
[smartcity-middleware v0.1.0.alpha](https://github.com/rbccps-iisc/smartcity-middleware-docker/releases/latest)

### Configuration:
`middleware.conf v0.1.0.alpha`

    DESCRIPTION

    middleware.conf is the configuration file for the smartcity-middleware application.
    KONG, RABBITMQ, TOMCAT, CATALOGUE docker containers requires a persistent data, config storage locations.

      DATA_STORAGE: Specify an empty directory in the system that docker will use for
      keeping data files. Here, providing separate directories for kong, rabbitmq, tomcat,
      catalogue is recommended.

      CONFIG_STORAGE: Specify an empty directory in the system that docker will use for
      keeping config files.

      SYSTEM_CONFIG specify system specific configurations for the installation steps.

      SSH_PUBLIC_KEY: Specify an ssh public key which will be used in ssh authentication
      of the user to docker containers.

      OS: Specify the OS used in the system. If you are using any linux distribution, give
      "linux" and if you are using macOS, give "macOS".

### Steps to Install:

After configuring the middleware.conf file, do the following steps.

1. **Installation of smart city middleware. This process will create all the required
docker containers.**

    Please satisfy the requirements mentioned in middleware.conf file.
    Password of the root user in docker containers for the alpha release is rbccps@123456.
    This will be removed in the later release.

        $ python smartcity-middleware.py install --config-file middleware.conf

    If the setup fails at any stage for reasons like for example internet connection issues, you can do the continue the failed installation using the following command.

        $ python smartcity-middleware.py install --config-file middleware.conf -l rabbitmq,tomcat,hypercat,kong,apt_repo

2. **Start smart city middleware.**

        $ python smartcity-middleware.py start

    or run `python smartcity-middleware.py -h` for more details.

3. **Serving smart city middleware on** https://localhost:8443

    The application will be serving with a self-signed certificate. If you want to use your certificate, have your .crt and .key file as config/kong/default_443.crt and config/kong/default_443.key respectively and do a fresh installation.

    All the GET, POST DELETE requests mentioned in https://rbccps.org/smartcity/doku.php, can be done on https://localhost:8443 .

| RBCCPS MIDDLEWARE API URLs                                     |      MIDDLEWARE API URLs                                 |
|----------------------------------------------------------------|----------------------------------------------------------|
| https://smartcity.rbccps.org/api/0.1.0/register                | https://localhost:8443/api/0.1.0/register                |
| https://smartcity.rbccps.org/api/0.1.0/publish                 | https://localhost:8443/api/0.1.0/publish                 |
| https://smartcity.rbccps.org/api/0.1.0/subscribe?name=testDemo | https://localhost:8443/api/0.1.0/subscribe?name=testDemo |
| https://smartcity.rbccps.org/api/0.1.0/subscribe/bind          | https://localhost:8443/api/0.1.0/subscribe/bind          |
| https://smartcity.rbccps.org/api/0.1.0/subscribe/unbind        | https://localhost:8443/api/0.1.0/subscribe/unbind        |
| https://smartcity.rbccps.org/api/0.1.0/cat                     | https://localhost:8443/api/0.1.0/cat                     |
| https://smartcity.rbccps.org/api/0.1.0/historicData            | https://localhost:8443/api/0.1.0/historicData            |

    For example, registration of device to local middleware is as follows.

    `curl -i -X GET "https://localhost:8443/api/0.1.0/register" -H 'apikey: <provider_api_key>' -H 'resourceID: <Your-Resource-ID>' -H 'serviceType: publish,subscribe,historicData' `


### NOTE:
  * Installation in Linux machines can fail for the following reasons.
     1. If you are in a corporate network that blocks Google DNS Servers, the `docker build` command fails.
        To fix it, add your corporate DNS servers in DOCKER_OPTS in /etc/default/docker.

        ` DOCKER_OPTS="--dns 208.67.222.222 --dns 208.67.220.220" `

        If this fails to set the DNS properly, try updating /etc/docker/daemon.json with the following

        ` { "dns": ["208.67.222.222", "208.67.220.220"] } `

        Also follow the steps mentioned in this issue https://github.com/moby/moby/issues/25357

     2. Set the bridge ip address to `172.18.0.1` in DOCKER_OPTS in /etc/default/docker.

           ` DOCKER_OPTS="--dns 208.67.222.222 --dns 208.67.220.220 --bip 172.18.0.1" `
     3. Make sure that the firewall rules are not blocking any access from container to the host machine.

   * Middleware has been tested on macOS as well.
     After satisfying the other requirements in middleware.conf, mention `OS=macOS` in middleware.conf. Then follow   instructions mentioned in Usage.

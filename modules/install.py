import subprocess
from utils import output_error, output_info, output_ok, output_warning
import traceback
import ConfigParser
import os


def remove_containers(log_file):
    """ Removes all existing docker containers with names like kong, rabbitmq. This is done to avoid any
    clash of names during the creation of containers.

    Args:
        log_file      (string): log file path
    """

    subprocess_with_print("docker rm kong",
                          success_msg="Removing Kong",
                          failure_msg="Kong container doesn't exist. SKIPPING THIS ERROR.",
                          log_file=log_file,
                          exit_on_fail=False)

    subprocess_with_print("docker rm apt_repo",
                          success_msg="Removing APT Repository",
                          failure_msg="APT Repository container doesn't exist. SKIPPING THIS ERROR.",
                          log_file=log_file,
                          exit_on_fail=False)

    subprocess_with_print("docker rm rabbitmq",
                          success_msg="Removing RabbitMQ",
                          failure_msg="RabbitMQ container doesn't exist. SKIPPING THIS ERROR.",
                          log_file=log_file,
                          exit_on_fail=False)

    subprocess_with_print("docker rm hypercat",
                          success_msg="Removing Catalogue server",
                          failure_msg="Catalogue server container doesn't exist. SKIPPING THIS ERROR.",
                          log_file=log_file,
                          exit_on_fail=False)

    subprocess_with_print("docker rm elasticsearch",
                          success_msg="Removing Elasticsearch",
                          failure_msg="Elasticsearch container doesn't exist. SKIPPING THIS ERROR.",
                          log_file=log_file,
                          exit_on_fail=False)

    subprocess_with_print("docker rm tomcat",
                          success_msg="Removing Tomcat",
                          failure_msg="Tomcat container doesn't exist. SKIPPING THIS ERROR.",
                          log_file=log_file,
                          exit_on_fail=False)

    subprocess_with_print("docker rm certificate_authority",
                          success_msg="Removing Certificate Authority",
                          failure_msg="Certificate Authority container doesn't exist. SKIPPING THIS ERROR.",
                          log_file=log_file,
                          exit_on_fail=False)

    subprocess_with_print("docker rm pushpin",
                          success_msg="Removing Pushpin",
                          failure_msg="Pushpin container doesn't exist. SKIPPING THIS ERROR.",
                          log_file=log_file,
                          exit_on_fail=False)


def stop_containers(log_file):
    """ Stops all existing docker containers like kong, rabbitmq, tomcat et cetera.

    Args:
        log_file      (string): log file path
    """
    subprocess_with_print("docker stop kong",
                          success_msg="Stopping Kong",
                          failure_msg="Kong container doesn't exist. SKIPPING THIS ERROR.",
                          log_file=log_file,
                          exit_on_fail=False)

    subprocess_with_print("docker stop apt_repo",
                          success_msg="Stopping APT Repository",
                          failure_msg="APT Repository container doesn't exist. SKIPPING THIS ERROR.",
                          log_file=log_file,
                          exit_on_fail=False)

    subprocess_with_print("docker stop rabbitmq",
                          success_msg="Stopping RabbitMQ",
                          failure_msg="RabbitMQ container doesn't exist. SKIPPING THIS ERROR.",
                          log_file=log_file,
                          exit_on_fail=False)

    subprocess_with_print("docker stop hypercat",
                          success_msg="Stopping Catalogue server",
                          failure_msg="Catalogue server container doesn't exist. SKIPPING THIS ERROR.",
                          log_file=log_file,
                          exit_on_fail=False)

    subprocess_with_print("docker stop elasticsearch",
                          success_msg="Stopping Elasticsearch",
                          failure_msg="Elasticsearch container doesn't exist. SKIPPING THIS ERROR.",
                          log_file=log_file,
                          exit_on_fail=False)

    subprocess_with_print("docker stop tomcat",
                          success_msg="Stopping Tomcat",
                          failure_msg="Tomcat container doesn't exist. SKIPPING THIS ERROR.",
                          log_file=log_file,
                          exit_on_fail=False)

    subprocess_with_print("docker stop certificate_authority",
                          success_msg="Stopping Certificate Authority",
                          failure_msg="Certificate Authority container doesn't exist. SKIPPING THIS ERROR.",
                          log_file=log_file,
                          exit_on_fail=False)

    subprocess_with_print("docker stop pushpin",
                          success_msg="Stopping Pushpin",
                          failure_msg="Pushpin container doesn't exist. SKIPPING THIS ERROR.",
                          log_file=log_file,
                          exit_on_fail=False)


def docker_setup(log_file, config_path="middleware.conf"):
    """ Creates docker instances for kong, ca, hypercat, rabbitmq, elastic search, apache storm, ldap, ntp and bind
    server from an ubuntu-ssh image. First, docker creates certificate authority (CA) instance and then have the CA
    certify Ansible user's public key. A new docker image with this CA's public key in TrustedUserCAKeys is created to
    avoid redundant sending of Ansible's public keys to all hosts.

    Important: This docker setup will remove all the current containers and there will be loss of data.
               This should be used only for fresh installation.

    """

    instance_details = {}
    config = ConfigParser.ConfigParser()
    config.readfp(open(config_path))

    subprocess_with_print("docker network create --driver bridge mynet",
                          success_msg="Created a docker network named mynet. ",
                          failure_msg="Already a docker network named mynet exists. ",
                          log_file=log_file,
                          exit_on_fail=False)

    kong_storage = config.get('KONG', 'DATA_STORAGE')
    output_info("Using {0} as Kong's persistant storage. ".format(kong_storage))
    kong_config_storage = config.get('KONG', 'CONFIG_STORAGE')
    output_info("Using {0} as Kong's config persistant storage. ".format(kong_config_storage))
    rabbitmq_storage = config.get('RABBITMQ', 'DATA_STORAGE')
    output_info("Using {0} as RabbitMQ's persistant storage. ".format(rabbitmq_storage))
    tomcat_storage = config.get('TOMCAT', 'DATA_STORAGE')
    output_info("Using {0} as Apache Tomcat's persistant storage. ".format(tomcat_storage))
    catalogue_storage = config.get('CATALOGUE', 'DATA_STORAGE')
    output_info("Using {0} as Catalogue's persistant storage. ".format(catalogue_storage))

    subprocess_with_print("docker build -t ansible/ubuntu-ssh -f images/Dockerfile.ubuntu .",
                          success_msg="Created ansible/ubuntu-ssh docker image. ",
                          failure_msg="Building ubuntu image from images/Dockerfile.ubuntu failed.",
                          log_file=log_file,
                          exit_on_fail=True)

    ca_ip, ca_port, details = create_instance("certificate_authority", "ansible/ubuntu-ssh", log_file)
    output_ok("Created Certificate Authority docker instance. \n " + details)

    instance_details["certificate_authority"] = [ca_ip, ca_port]
    create_ansible_host_file(instance_details)
    output_ok("Created Ansible hosts file with CA instance. ")

    key = config.get('SYSTEM_CONFIG', 'SSH_PUBLIC_KEY')
    output_info("Using {0} as your ssh key for certification. ".format(key))

    home = os.path.expanduser('~')
    with open(home + "/.ssh/configs", 'w+') as f:
        f.write("IdentityFile {0}\n".format(key))
    key = key.replace("~", home)
    cmd = 'cp -r ' + key + ' ' + os.getcwd() + '/config/certificate_authority/keys/id_rsa.pub'
    subprocess_popen(cmd, log_file, "Copying to /config/certificate_authority/keys/ failed.")

    cmd = 'ssh-copy-id -i {0} root@{1} -p {2}'.format(key, ca_ip, ca_port[1:-1])
    subprocess_popen(cmd, log_file, "Copying SSH Public-key to Certificate Authority failed.")
    output_ok("Copied SSH Public-key to Certificate Authority. ")

    output_info("Starting Ansible Certificate Authority Setup. ")
    subprocess.call('ansible-playbook -i hosts install.yaml --limit "certificate_authority"',
                    shell=True)

    cmd = "cp config/certificate_authority/keys/id_rsa-cert.pub " + "~/.ssh/".replace("~", home)
    subprocess_popen(cmd, log_file, "Copying Certificate Authority's cert file to ansible's .ssh/ failed.")
    output_ok("Copied Certificate Authority's cert file to Ansible's .ssh. ")

    subprocess_with_print("docker build -t ansible/ubuntu-certified:1.0 -f images/Dockerfile.ubuntu.certified .",
                          success_msg="Created ansible/ubuntu-certified:1.0 docker image. ",
                          failure_msg="Building ubuntu image from images/Dockerfile.ubuntu.certified failed.",
                          log_file=log_file,
                          exit_on_fail=True)

    cmd = "docker build -t ansible/ubuntu-certified-aptrepo:1.0 -f " \
          "images/Dockerfile.ubuntu.certified.aptrepo.readytoserve ."
    subprocess_with_print(cmd,
                          success_msg="Created ansible/ubuntu-certified-aptrepo:1.0 docker image. ",
                          failure_msg="Building ubuntu image from "
                                      "images/Dockerfile.ubuntu.certified.aptrepo.readytoserve failed.",
                          log_file=log_file,
                          exit_on_fail=True)

    cmd = "docker build -t ansible/ubuntu-certified-catalogue:1.0 -f images/Dockerfile.ubuntu.certified.catalogue ."
    subprocess_with_print(cmd,
                          success_msg="Created ansible/ubuntu-certified-catalogue:1.0 docker image. ",
                          failure_msg="Building ubuntu image from images/Dockerfile.ubuntu.certified.catalogue failed.",
                          log_file=log_file,
                          exit_on_fail=True)

    cmd = "docker build -t ansible/ubuntu-certified-kong:1.0 -f images/Dockerfile.ubuntu.certified.kong ."
    subprocess_with_print(cmd,
                          success_msg="Created ansible/ubuntu-certified-kong:1.0 docker image. ",
                          failure_msg="Building ubuntu image from images/Dockerfile.ubuntu.certified.kong failed.",
                          log_file=log_file,
                          exit_on_fail=True)
    cmd = "docker build -t ansible/ubuntu-certified-rabbitmq:1.0 -f images/Dockerfile.ubuntu.certified.rabbitmq ."
    subprocess_with_print(cmd,
                          success_msg="Created ansible/ubuntu-certified-rabbitmq:1.0 docker image. ",
                          failure_msg="Building ubuntu image from images/Dockerfile.ubuntu.certified.rabbitmq failed.",
                          log_file=log_file,
                          exit_on_fail=True)
    failure_msg = "Building ansible/pushpin image from images/Dockerfile.ubuntu.certified.pushpin failed."
    subprocess_with_print("docker build -t ansible/pushpin -f images/Dockerfile.ubuntu.certified.pushpin .",
                          success_msg="Created ansible/pushpin docker image. ",
                          failure_msg=failure_msg,
                          log_file=log_file,
                          exit_on_fail=True)

    subprocess_with_print("docker build -t ansible/tomcat -f images/Dockerfile.tomcat .",
                          success_msg="Created ansible/tomcat docker image. ",
                          failure_msg="Building ansible/tomcat image from images/Dockerfile.tomcat failed.",
                          log_file=log_file,
                          exit_on_fail=True)

    ip, port, details = create_instance("apt_repo", "ansible/ubuntu-certified-aptrepo:1.0", log_file)
    instance_details["apt_repo"] = [ip, port]
    output_ok("Created Apt Local Repository docker instance. \n " + details)

    ip, port, details = create_instance("kong", "ansible/ubuntu-certified-kong:1.0",
                                        storage_host=kong_storage,
                                        storage_guest="/var/lib/postgresql",
                                        log_file=log_file)

    instance_details["kong"] = [ip, port]
    output_ok("Created Kong docker instance. \n " + details)

    ip, port, details = create_instance("hypercat", "ansible/ubuntu-certified-catalogue:1.0",
                                        storage_host=catalogue_storage,
                                        storage_guest="/data/db",
                                        log_file=log_file)
    instance_details["hypercat"] = [ip, port]
    output_ok("Created Catalogue docker instance. \n " + details)

    ip, port, details = create_instance("rabbitmq", "ansible/ubuntu-certified-rabbitmq:1.0",
                                        storage_host=rabbitmq_storage,
                                        storage_guest="/var/lib/rabbitmq",
                                        log_file=log_file)
    instance_details["rabbitmq"] = [ip, port]
    output_ok("Created RabbitMQ docker instance. \n " + details)

    ip, port, details = create_instance("elasticsearch", "ansible/ubuntu-certified:1.0", log_file=log_file)
    instance_details["elasticsearch"] = [ip, port]
    output_ok("Created Elastic Search docker instance. \n " + details)

    ip, port, details = create_instance("tomcat", "ansible/tomcat",
                                        storage_host=tomcat_storage,
                                        storage_guest="/opt/tomcat/webapps",
                                        log_file=log_file)
    instance_details["tomcat"] = [ip, port]
    output_ok("Created Tomcat docker instance. \n " + details)

    if config.get('SYSTEM_CONFIG', 'OS') == "linux":
        cmd = "cp config/tomcat/RegisterAPIDocker.war " + tomcat_storage + "/RegisterAPI.war"
        subprocess_popen(cmd, log_file, "Copying RegisterAPIDocker.war file to {0} failed.".format(tomcat_storage))
        output_ok("Copied  RegisterAPIDocker.war file to {0}. ".format(tomcat_storage))
    elif config.get('SYSTEM_CONFIG', 'OS') == "macOS":
        cmd = "cp config/tomcat/RegisterAPIMAC.war " + tomcat_storage + "/RegisterAPI.war"
        subprocess_popen(cmd, log_file, "Copying RegisterAPIMAC.war file to {0} failed.".format(tomcat_storage))
        output_ok("Copied  RegisterAPIMAC.war file to {0}. ".format(tomcat_storage))

    cmd = "docker run -d -p 8443:443 --net mynet --hostname={0} --cap-add=NET_ADMIN --name {0} {1}".\
        format("pushpin", "ansible/pushpin")
    subprocess_with_print(cmd,
                          success_msg="Created Pushpin docker instance. ",
                          failure_msg="Creation of Pushpin docker instance failed.",
                          log_file=log_file,
                          exit_on_fail=True)

    cmd = 'docker run -d ' \
          '-p 31337:1337 ' \
          '--net mynet ' \
          '--hostname=konga ' \
          '--link kong:kong ' \
          '--name konga ' \
          '-e "NODE_ENV=production" ' \
          'pantsel/konga'

    subprocess_with_print(cmd,
                          success_msg="Created KONGA docker instance. ",
                          failure_msg="Creation of KONGA docker instance failed.",
                          log_file=log_file,
                          exit_on_fail=True)
    create_ansible_host_file(instance_details)


def create_instance(server, image, log_file, storage_host="", storage_guest=""):
    """ Create a docker instance from the image provided with persistent storages.

    Args:
        server        (string): docker instance name
        image         (string): docker image name
        log_file      (string): log file path
        storage_host  (string): mount point created in the server for persistent storage
        storage_guest (string): location inside docker where the persistent storage occurs
    """
    port = ""
    container_id = ""

    if server in ["kong", "rabbitmq", "hypercat", "tomcat"]:  # separate storage needed cases
        cmd = "docker run -d -P --net=mynet --hostname={0} -v {2}:{3} --cap-add=NET_ADMIN --name={0} {1}".\
            format(server, image, storage_host, storage_guest)

        try:
            out, err = subprocess_popen(cmd,
                                        log_file,
                                        failure_msg="Creation of {0} docker instance failed.".format(server))
            container_id = out
        except OSError:
            output_error("Creation of {0} docker instance failed.".format(server) +
                         "\n           Check logs {0} for more details.".format(log_file),
                         error_message=traceback.format_exc())
            exit()

    else:
        cmd = "docker run -d -P --net=mynet --hostname={0} --cap-add=NET_ADMIN --name={0} {1}".format(server, image)
        try:
            out, err = subprocess_popen(cmd,
                                        log_file,
                                        failure_msg="Creation of {0} docker instance failed.".format(server))
            container_id = out
        except OSError:
            output_error("Creation of {0} docker instance failed.".format(server) +
                         "\n           Check logs {0} for more details.".format(log_file),
                         error_message=traceback.format_exc())
            exit()

    # Code to figure out port of the docker container
    # docker inspect --format='{{(index (index .NetworkSettings.Ports "22/tcp") 0).HostPort}}'
    # (index .NetworkSettings.Ports "22/tcp") gives an array whose 0th element has .HostPort value
    try:
        p = subprocess.Popen(['docker',
                             'inspect',
                              """--format='{{(index (index .NetworkSettings.Ports "22/tcp") 0).HostPort}}'""",
                              server], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdoutdata, stderrdata = p.communicate()

        if p.returncode != 0:
            output_error("Creation of {0} docker instance failed, when port address was fetched.".format(server) +
                         "\n           Check logs {0} for more details.".format(log_file),
                         error_message=stderrdata, stdout=stdoutdata)
            exit()
        port = stdoutdata
    except OSError:
        output_error("Creation of {0} docker instance failed.".format(server) +
                     "\n           Check logs {0} for more details.".format(log_file),
                     error_message=traceback.format_exc())
        exit()

    details = "\n"
    details += " DOCKER INSTANCE\n"
    details += " {0} docker name         : {1}\n".format(server, server)
    details += " {0} docker container ID : {1}\n".format(server, container_id.rstrip())
    details += " {0} IP address          : 'localhost' \n".format(server)
    details += " {0} SSH Port            : {1} \n".format(server, str(port))

    return "localhost", port.rstrip(), details


def create_ansible_host_file(instances):
    """ Creates an inventory file named hosts for ansible in the current directory. Inventory file will contain
    IP address, port and ssh_username of the all the hosts (docker containers) mentioned in instances parameter.

    Args:
        instances (dict): instances is a dict of the form { 'server' : [IPAddress, Port]}.
    """
    hosts_list = []
    for key, value in instances.iteritems():
        hosts_list.append("{0} ansible_host={1} ansible_port={2} ansible_user=root".format(key, value[0], value[1]))

    hosts_contents = "\n".join(hosts_list)

    with open('hosts', 'w+') as host_file:
        host_file.write(hosts_contents)


def check_dependencies(log_file):
    """ Checks for system dependencies.

    Args:
        log_file      (string): log file path
    """
    subprocess_with_print("docker -v",
                          success_msg="Docker is installed. ",
                          failure_msg="Docker is not installed. Please install docker",
                          log_file=log_file,
                          exit_on_fail=True)

    subprocess_with_print("vagrant -v",
                          success_msg="Vagrant is installed. ",
                          failure_msg="Vagrant is not installed. Please install Vagrant",
                          log_file=log_file,
                          exit_on_fail=True)

    subprocess_with_print("virtualbox -h",
                          success_msg="Virtualbox is installed. ",
                          failure_msg="Virtualbox is not installed. Please install Virtualbox",
                          log_file=log_file,
                          exit_on_fail=True)


def ansible_setup(limit=""):
    """ Creates all the plays/installation from ansible install.yaml file.

    Args:
         limit (string):  Limits the ansible installation to the servers mentioned.
                          A comma separated list of servers like --limit kong, rabbitmq
    """
    output_info("Starting Ansible setup. ")
    subprocess.call('ansible-playbook -i hosts install.yaml --limit "' + limit + '"', shell=True)


def subprocess_with_print(cmd, success_msg, failure_msg, log_file, exit_on_fail=False):
    """ Create a subprocess call and outputs success and errors if any.

    Args:
        cmd          (string): docker instance name
        success_msg  (string): success message to be displayed in [OK] format.
        failure_msg  (string): failure text to be displayed with [FAILED] format.
        log_file     (string): log file path
        exit_on_fail (bool): exit program if failed
    """
    try:
        process = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output_ok(success_msg, message=process.stdout.read(), stderr=process.stderr.read())
    except OSError:
        if exit_on_fail:
            output_error(failure_msg + "\n           Check logs {0} for more details.".format(log_file),
                         error_message=traceback.format_exc())
            exit()
        else:
            output_warning(failure_msg + "\n           Check logs {0} for more details.".format(log_file),
                           error_message=traceback.format_exc())


def subprocess_popen(cmd, log_file, failure_msg):
    """ Create a subprocess call and outputs errors if any.

    Args:
        cmd         (string): docker instance name
        log_file    (string): log file path
        failure_msg (string): failure text
    """
    p = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        output_error(failure_msg + "\n           Check logs {0} for more details.".format(log_file),
                     error_message=stderr, stdout=stdout)
        exit()
    return stdout, stderr

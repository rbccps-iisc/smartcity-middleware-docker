import subprocess
from utils import output_error, output_info, output_ok, output_warning
import traceback
import ConfigParser
import os
from time import time


def remove_containers(list,log_file):
    """ Removes all existing docker containers with names like kong, rabbitmq. This is done to avoid any
    clash of names during the creation of containers.

    Args:
        log_file      (string): log file path
    """
    for container in list:
        subprocess_with_print("docker rm {0}".format(container),
                              success_msg="Removing {0}".format(container),
                              failure_msg="{0} container doesn't exist. SKIPPING THIS ERROR.".format(container),
                              log_file=log_file,
                              exit_on_fail=False)

    subprocess_with_print("docker volume rm ldapd-data",
                          success_msg="Removed ldapd-data volume",
                          failure_msg="Ldapd-data volume doesn't exist. SKIPPING THIS ERROR.",
                          log_file=log_file,
                          exit_on_fail=False)


def stop_containers(list,log_file):
    """ Stops all existing docker containers like kong, rabbitmq, tomcat .

    Args:
        log_file      (string): log file path
    """
    for container in list:

        subprocess_with_print("docker stop {0}".format(container),
                              success_msg="Stopping {0}".format(container),
                              failure_msg="{0} container doesn't exist. SKIPPING THIS ERROR.".format(container),
                              log_file=log_file,
                              exit_on_fail=False)


def unique_value():
    return str(int(time()))


def docker_setup(log_file, config_path="/etc/ideam/ideam.conf"):
    """ Creates docker instances for kong, ca, catalogue, rabbitmq, elastic search, apache storm, ldap, ntp and bind
    server from an ubuntu-ssh image. First, docker creates certificate authority (CA) instance and then have the CA
    certify Ansible user's public key. A new docker image with this CA's public key in TrustedUserCAKeys is created to
    avoid redundant sending of Ansible's public keys to all hosts.

    Important: This docker setup will remove all the current containers and there will be loss of data.
               This should be used only for fresh installation.

    """
    config = ConfigParser.ConfigParser()
    config.readfp(open(config_path))

    subprocess_with_print("docker network create --driver bridge mynet",
                          success_msg="Created a docker network named mynet. ",
                          failure_msg="Already a docker network named mynet exists. ",
                          log_file=log_file,
                          exit_on_fail=False)

    kong_storage = config.get('KONG', 'DATA_STORAGE')
    kong_log_location = config.get('KONG', 'LOG_LOCATION')
    output_info("Using {0} as Kong's persistent storage. ".format(kong_storage))
    kong_config_storage = config.get('KONG', 'CONFIG_STORAGE')
    output_info("Using {0} as Kong's config persistent storage. ".format(kong_config_storage))
    rabbitmq_storage = config.get('RABBITMQ', 'DATA_STORAGE')
    output_info("Using {0} as RabbitMQ's persistent storage. ".format(rabbitmq_storage))
    tomcat_storage = config.get('TOMCAT', 'DATA_STORAGE')
    output_info("Using {0} as Apache Tomcat's persistent storage. ".format(tomcat_storage))
    catalogue_storage = config.get('CATALOGUE', 'DATA_STORAGE')
    output_info("Using {0} as Catalogue's persistent storage. ".format(catalogue_storage))

    subprocess_with_print("docker volume create --name ldapd-data",
                          success_msg="Created ldapd-data data container ",
                          failure_msg="Creation of ldapd-data data container failed.",
                          log_file=log_file,
                          exit_on_fail=True)

    # key = config.get('SYSTEM_CONFIG', 'SSH_PUBLIC_KEY')
    # output_info("Using {0} as your ssh key for certification. ".format(key))
    # home = os.path.expanduser('~')
    # with open(home + "/.ssh/configs", 'w+') as f:
    #     f.write("IdentityFile {0}\n".format(key))
    # key = key.replace("~", home)
    #
    # subprocess_popen("find "+key, log_file, "Missing ssh public key file in {}. Create one using command ssh-keygen.".
    #                  format(key))
    # cmd = 'cp -r ' + key + ' ' + os.getcwd() + '/config/certificate_authority/keys/id_rsa.pub'
    # subprocess_popen(cmd, log_file, "Copying to /config/certificate_authority/keys/ failed.")

    # subprocess_with_print("docker build -t ideam/alpine-ssh -f images/alpine/Dockerfile.alpine-ssh .".
    #                       format(unique_value()),
    #                       success_msg="Created ideam/alpine-ssh docker image. ",
    #                       failure_msg="Building alpine image from images/alpine/Dockerfile.alpine-ssh failed.",
    #                       log_file=log_file,
    #                       exit_on_fail=True)
    #
    # ca_ip, ca_port, details = create_instance("certificate_authority", "ideam/alpine-ssh", log_file, config_path=config_path)
    # output_ok("Created Certificate Authority docker instance. \n " + details)
    #
    # instance_details["certificate_authority"] = [ca_ip, ca_port]
    # create_ansible_host_file(instance_details)
    # output_ok("Created Ansible hosts file with CA instance. ")
    #
    # output_info("Starting Ansible Certificate Authority Setup. ")
    # subprocess.call('tasks/certificate_authority/ca.sh '+str(subprocess.check_output("docker port certificate_authority | grep 22 | cut -d : -f 2",shell=True)).strip(),
    #                 shell=True)
    #
    # cmd = "cp config/certificate_authority/keys/id_rsa-cert.pub " + "~/.ssh/".replace("~", home)
    # subprocess_popen(cmd, log_file, "Copying Certificate Authority's cert file to ansible's .ssh/ failed.")
    # output_ok("Copied Certificate Authority's cert file to Ansible's .ssh. ")

#TODO change data folder of postgres
    ip, details = create_instance("kong", "ideam/kong",
                                        storage_host=kong_storage,
                                        storage_guest="/var/lib/postgresql",
                                        log_file=log_file,
                                        config_path=config_path,
                                        log_storage=kong_log_location)

    output_ok("Created Kong docker instance. \n " + details)

    ip, details = create_instance("catalogue", "ideam/catalogue",
                                        storage_host=catalogue_storage,
                                        storage_guest="/data/db",
                                        log_file=log_file,
                                        config_path=config_path)

    output_ok("Created Catalogue docker instance. \n " + details)

    ip, details = create_instance("rabbitmq", "ideam/rabbitmq",
                                        storage_host=rabbitmq_storage,
                                        storage_guest="/var/lib/rabbitmq",
                                        log_file=log_file,
                                        config_path=config_path)

    output_ok("Created RabbitMQ docker instance. \n " + details)

    ip, details = create_instance("elasticsearch", "ideam/elasticsearch-nokibana", log_file=log_file, config_path=config_path)

    output_ok("Created Elastic Search docker instance. \n " + details)

    ip, details = create_instance("tomcat", "ideam/tomcat",
                                        storage_host=tomcat_storage,
                                        storage_guest="/usr/local/tomcat/webapps",
                                        log_file=log_file,
                                        config_path=config_path)

    output_ok("Created Tomcat docker instance. \n " + details)

    ip, details = create_instance("ldapd", "ideam/ldapd",
                                        storage_host="ldapd-data",
                                        storage_guest="/var/db",
                                        log_file=log_file,
                                        config_path=config_path)

    output_ok("Created LDAP docker instance. \n " + details)

    ip, details = create_instance("videoserver", "ideam/videoserver", log_file=log_file, config_path=config_path)

    output_ok("Created Videoserver docker instance. \n " + details)

    konga = config.get('KONGA', 'HTTP')
    cmd = 'docker run -d -p {0}:1337 --net mynet --link kong:kong --name konga -e "NODE_ENV=production" pantsel/konga'.\
        format(konga)
    subprocess_with_print(cmd,
                          success_msg="Created KONGA docker instance. ",
                          failure_msg="Creation of KONGA docker instance failed.",
                          log_file=log_file,
                          exit_on_fail=True)

    for container in ["kong","rabbitmq","ldapd","catalogue","videoserver","tomcat","elasticsearch"]:

        print("") #Just to separate out the individual installations
        output_info("Starting {0} installation".format(container))
        subprocess.call('tasks/{0}/setup.sh'.format(container), shell=True)
        output_ok("Installed {0}".format(container))


def create_instance(server, image, log_file, storage_host="", storage_guest="", config_path="/etc/ideam/ideam.conf",
                    log_storage=""):
    """ Create a docker instance from the image provided with persistent storages.

    Args:
        server        (string): docker instance name
        image         (string): docker image name
        log_file      (string): log file path
        storage_host  (string): mount point created in the server for persistent storage
        storage_guest (string): location inside docker where the persistent storage occurs
        config_path   (string): location of config file
        log_storage   (string): storage space for logs
    """
    port = ""
    container_id = ""
    config = ConfigParser.ConfigParser()
    config.readfp(open(config_path))

    if server == "kong":  # separate kong log storage needed

        cmd = "docker run -d -p 80:8000 --net=mynet --hostname={0} " \
              "-v {2}:{3} -v {4}:/tmp --cap-add=NET_ADMIN --name={0} {1}".\
            format(server, image, storage_host, storage_guest, log_storage)

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
    elif server == "rabbitmq":  # separate rabbitmq log storage needed
        #TODO: have only amqps, mqtts and https
        http = config.get('RABBITMQ', 'HTTP')
        amqp = config.get('RABBITMQ', 'AMQP')
        mqtt = config.get('RABBITMQ', 'MQTT')
        log_storage = config.get('RABBITMQ', 'LOG_LOCATION')
        management = config.get('RABBITMQ', 'MANAGEMENT')

        cmd = "docker run -d -p {4}:8000 -p {5}:5672 -p {6}:1883 -p {7}:15672 --net=mynet --hostname={0}" \
              " -v {2}:{3} -v {8}:/var/log/rabbitmq -v {8}:/var/log/supervisor --cap-add=NET_ADMIN --name={0} {1}".\
            format(server, image, storage_host, storage_guest, http, amqp, mqtt, management, log_storage)

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
    elif server == "tomcat":  # separate tomcat log storage needed
        http = config.get('TOMCAT', 'HTTP')
        log_storage = config.get('TOMCAT', 'LOG_LOCATION')
        cmd = "docker run -d -p {4}:8080 --net=mynet --hostname={0} -v {2}:{3}" \
              " --cap-add=NET_ADMIN --name={0} {1}".\
            format(server, image, storage_host, storage_guest, http, log_storage)

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
    elif server == "catalogue":  # separate data storage needed
        http = config.get('CATALOGUE', 'HTTP')
        cmd = "docker run -d -p {4}:8000 --net=mynet --hostname={0} " \
              "-v {2}:{3} --cap-add=NET_ADMIN --name={0} {1}".\
            format(server, image, storage_host, storage_guest, http)

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
    elif server == "ldapd":  # separate data storage needed
        ldap = config.get('LDAP', 'LDAP')
        cmd = "docker run -d -p {4}:8389 --net=mynet --hostname={0} " \
              "-v {2}:{3} --cap-add=NET_ADMIN --name={0} {1}".\
            format(server, image, storage_host, storage_guest, ldap)

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

    elif server == "elasticsearch":
        kibana = config.get('ELASTICSEARCH', 'KIBANA')
        cmd = "docker run -d -p {2}:5601 --net=mynet " \
              "--hostname={0} --cap-add=NET_ADMIN --name={0} {1}".format(server, image, kibana)
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
    elif server == "videoserver":
        rtmp = config.get('VIDEOSERVER', 'RTMP')
        hls = config.get('VIDEOSERVER', 'HLS')
        http = config.get('VIDEOSERVER', 'HTTP')
        cmd = "docker run -d -p {1}:1935 -p {2}:8080 -p {3}:8088 --net=mynet --hostname={0} --privileged --cap-add=ALL --name={0} {4}". \
            format("videoserver", rtmp, hls, http, image)
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
    # try:
    #     p = subprocess.Popen(['docker',
    #                          'inspect',
    #                           """--format='{{(index (index .NetworkSettings.Ports "22/tcp") 0).HostPort}}'""",
    #                           server], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #     stdoutdata, stderrdata = p.communicate()
    #
    #     if p.returncode != 0:
    #         output_error("Creation of {0} docker instance failed, when port address was fetched.".format(server) +
    #                      "\n           Check logs {0} for more details.".format(log_file),
    #                      error_message=stderrdata, stdout=stdoutdata)
    #         exit()
    #     port = stdoutdata
    # except OSError:
    #     output_error("Creation of {0} docker instance failed.".format(server) +
    #                  "\n           Check logs {0} for more details.".format(log_file),
    #                  error_message=traceback.format_exc())
    #     exit()

    details = "\n"
    details += " DOCKER INSTANCE\n"
    details += " {0} docker name         : {1}\n".format(server, server)
    details += " {0} docker container ID : {1}\n".format(server, container_id.rstrip())

    return "localhost", details


# def create_ansible_host_file(instances):
#     """ Creates an inventory file named hosts for ansible in the current directory. Inventory file will contain
#     IP address, port and ssh_username of the all the hosts (docker containers) mentioned in instances parameter.
#
#     Args:
#         instances (dict): instances is a dict of the form { 'server' : [IPAddress, Port] }.
#     """
#     hosts_list = []
#     for key, value in instances.iteritems():
#         hosts_list.append("{0} ansible_host={1} ansible_port={2} ansible_user=root".format(key, value[0], value[1]))
#
#     hosts_contents = "\n".join(hosts_list)
#     print(hosts_contents)
#     with open('hosts', 'w+') as host_file:
#         host_file.write(hosts_contents)

def limit_install(list):

    for container in list:
        output_info("Starting {0} installation".format(container))
        subprocess.call('tasks/{0}/setup.sh',shell=True)
        output_ok("Installed {0}".format(container))


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


# def ansible_installation(limit):
#     """ Creates all the plays/installation from ansible install.yaml file.
#
#     Args:
#          limit (string):  Limits the ansible installation to the servers mentioned.
#                           A comma separated list of servers like --limit kong, rabbitmq
#     """
#     output_info("Starting Ansible setup. ")
#     # subprocess.call('ansible-playbook -i \'localhost\' -s install_idps.yml --ask-sudo-pass')
#     subprocess.call('ansible-playbook -i hosts install.yaml --limit "' + limit + '"', shell=True)


def subprocess_with_print(cmd, success_msg, failure_msg, log_file, exit_on_fail=False):
    """ Create a subprocess call and outputs success and errors if any.

    Args:
        cmd          (string): docker instance name
        success_msg  (string): success message to be displayed in [OK] format.
        failure_msg  (string): failure text to be displayed with [FAILED] format.
        log_file     (string): log file path
        exit_on_fail   (bool): exit program if failed
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

    cmd = cmd.replace(";","")
    cmd = cmd.replace("|","")
    cmd = cmd.replace("$","")
    cmd = cmd.replace("{","")
    cmd = cmd.replace("}","")

    p = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        output_error(failure_msg + "\n           Check logs {0} for more details.".format(log_file),
                     error_message=stderr, stdout=stdout)
        exit()
    return stdout, stderr

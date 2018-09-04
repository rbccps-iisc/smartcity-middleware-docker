import subprocess
from utils import output_error, output_info, output_ok, output_warning
import traceback
import ConfigParser
import os
from time import time


def remove_containers(list,log_file):

    for container in list:
        subprocess_with_print("docker rm {0}".format(container),
                              success_msg="Removing {0}".format(container),
                              failure_msg="{0} container doesn't exist. SKIPPING THIS ERROR.".format(container),
                              log_file=log_file,
                              exit_on_fail=False)

def remove_volumes(list,log_file):

    for volume in list:
        subprocess_with_print("docker volume rm {0}-data".format(volume),
                              success_msg="Removed {0}-data volume".format(volume),
                              failure_msg="{0}-data volume doesn't exist. SKIPPING THIS ERROR.".format(volume),
                              log_file=log_file,
                              exit_on_fail=False)

def stop_containers(list,log_file):

    for container in list:

        subprocess_with_print("docker stop {0}".format(container),
                              success_msg="Stopping {0}".format(container),
                              failure_msg="{0} container doesn't exist. SKIPPING THIS ERROR.".format(container),
                              log_file=log_file,
                              exit_on_fail=False)


def unique_value():
    return str(int(time()))

def docker_setup(log_file, config_path="/etc/ideam/ideam.conf"):

    config = ConfigParser.ConfigParser()
    config.readfp(open(config_path))

    subprocess_with_print("docker network create --driver bridge mynet",
                          success_msg="Created a docker network named mynet. ",
                          failure_msg="Already a docker network named mynet exists. ",
                          log_file=log_file,
                          exit_on_fail=False)

    output_info("Using apigateway-data as apigateway's persistent storage.")
    output_info("Using broker-data as broker's persistent storage.")
    output_info("Using webserver-data as webserver's persistent storage.")
    output_info("Using catalogue-data as Catalogue's persistent storage.")

    subprocess_with_print("docker volume create --name ldapd-data",
                          success_msg="Created ldapd-data data container ",
                          failure_msg="Creation of ldapd-data data container failed.",
                          log_file=log_file,
                          exit_on_fail=True)

    subprocess_with_print("docker volume create --name apigateway-data",
                          success_msg="Created apigateway-data data container ",
                          failure_msg="Creation of apigateway-data data container failed.",
                          log_file=log_file,
                          exit_on_fail=True)

    subprocess_with_print("docker volume create --name broker-data",
                          success_msg="Created broker-data data container ",
                          failure_msg="Creation of broker-data data container failed.",
                          log_file=log_file,
                          exit_on_fail=True)

    subprocess_with_print("docker volume create --name cat-data",
                          success_msg="Created cat-data data container ",
                          failure_msg="Creation of cat-data data container failed.",
                          log_file=log_file,
                          exit_on_fail=True)

    subprocess_with_print("docker volume create --name elk-data",
                          success_msg="Created elk-data data container ",
                          failure_msg="Creation of elk-data data container failed.",
                          log_file=log_file,
                          exit_on_fail=True)

    subprocess_with_print("docker volume create --name webserver-data",
                          success_msg="Created webserver-data data container ",
                          failure_msg="Creation of webserver-data data container failed.",
                          log_file=log_file,
                          exit_on_fail=True)

    ip, details = create_instance("apigateway", "ideam/apigateway",
                                        storage_host="apigateway-data",
                                        storage_guest="/var/lib/postgresql/",
                                        log_file=log_file,
                                        config_path=config_path)

    output_ok("Created apigateway docker instance. \n " + details)

    ip, details = create_instance("catalogue", "ideam/catalogue",
                                        storage_host="cat-data",
                                        storage_guest="/data/db",
                                        log_file=log_file,
                                        config_path=config_path)

    output_ok("Created Catalogue docker instance. \n " + details)

    ip, details = create_instance("broker", "ideam/broker",
                                        storage_host="broker-data",
                                        storage_guest="/var/lib/rabbitmq/",
                                        log_file=log_file,
                                        config_path=config_path)

    output_ok("Created Broker docker instance. \n " + details)

    ip, details = create_instance("elasticsearch", "ideam/elasticsearch",
                                  storage_host="elk-data",
                                  storage_guest="/home/ideam/elasticsearch-6.2.4",
                                  log_file=log_file,
                                  config_path=config_path)

    output_ok("Created Elastic Search docker instance. \n " + details)

    ip, details = create_instance("webserver", "ideam/webserver",
                                        storage_host="webserver-data",
                                        storage_guest="/usr/local/webserver/",
                                        log_file=log_file,
                                        config_path=config_path)

    output_ok("Created Webserver docker instance. \n " + details)

    ip, details = create_instance("ldapd", "ideam/ldapd",
                                        storage_host="ldapd-data",
                                        storage_guest="/var/db",
                                        log_file=log_file,
                                        config_path=config_path)

    output_ok("Created LDAP docker instance. \n " + details)

    ip, details = create_instance("videoserver", "ideam/videoserver", log_file=log_file, config_path=config_path)

    output_ok("Created Videoserver docker instance. \n " + details)

    konga = config.get('KONGA', 'HTTP')
    cmd = 'docker run -d -p 127.0.0.1:{0}:1337 --net mynet --link apigateway:kong --name konga -e "NODE_ENV=production" pantsel/konga'.\
        format(konga)
    subprocess_with_print(cmd,
                          success_msg="Created KONGA docker instance. ",
                          failure_msg="Creation of KONGA docker instance failed.",
                          log_file=log_file,
                          exit_on_fail=True)

    for container in ["apigateway","broker","ldapd","catalogue","videoserver","webserver","elasticsearch"]:

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

    if server == "apigateway":  # separate apigateway log storage needed

        cmd = "docker run -d -p 8443:8443 -v {2}:{3} --net=mynet --hostname={0} " \
              "--cap-add=NET_ADMIN --name={0} {1}". \
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
    elif server == "broker":  # separate rabbitmq log storage needed

        #TODO: have only amqps, mqtts and https

        http = config.get('BROKER', 'HTTP')
        amqp = config.get('BROKER', 'AMQP')
        mqtt = config.get('BROKER', 'MQTT')
        management = config.get('BROKER', 'MANAGEMENT')

        cmd = "docker run -d -v {2}:{3} -p 127.0.0.1:{4}:8000 -p {5}:5672 -p {6}:1883 -p 127.0.0.1:{7}:15672 --net=mynet --hostname={0}" \
              " --cap-add=NET_ADMIN --name={0} {1}". \
            format(server, image, storage_host, storage_guest, http, amqp, mqtt, management)

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

    elif server == "webserver":  # separate webserver log storage needed

        http = config.get('WEBSERVER', 'HTTP')
        
        cmd = "docker run -d -v {2}:{3} -p 127.0.0.1:{4}:8080 --net=mynet --hostname={0}" \
              " --cap-add=NET_ADMIN --name={0} {1}".format(server, image, storage_host, storage_guest, http)

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

        cmd = "docker run -d -v {2}:{3} -p 127.0.0.1:{4}:8000 --net=mynet --hostname={0} " \
              "--cap-add=NET_ADMIN --name={0} {1}". \
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

        cmd = "docker run -d -p 127.0.0.1:{4}:8389 --net=mynet --hostname={0} " \
              "-v {2}:{3} --cap-add=NET_ADMIN --name={0} {1}". \
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
        cmd = "docker run -d -v {2}:{3} --net=mynet " \
              "--hostname={0} --cap-add=NET_ADMIN -p 127.0.0.1:{4}:5601 --name={0} {1}".format(server, image, storage_host, storage_guest, kibana)
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

    details = "\n"
    details += " DOCKER INSTANCE\n"
    details += " {0} docker name         : {1}\n".format(server, server)
    details += " {0} docker container ID : {1}\n".format(server, container_id.rstrip())

    return "localhost", details

def limit_install(list):

    for container in list:
        output_info("Starting {0} installation".format(container))
        subprocess.call('tasks/{0}/setup.sh'.format(container),shell=True)
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

def subprocess_with_print(cmd, success_msg, failure_msg, log_file, exit_on_fail=False):
    """ Create a subprocess call and outputs success and errors if any.

    Args:
        cmd          (string): docker instance name
        success_msg  (string): success message to be displayed in [OK] format.
        failure_msg  (string): failure text to be displayed with [FAILED] format.
        log_file     (string): log file path
        exit_on_fail   (bool): exit program if failed
    """

    cmd = cmd.replace(";", "")
    cmd = cmd.replace("|", "")
    cmd = cmd.replace("$", "")
    cmd = cmd.replace("{", "")
    cmd = cmd.replace("}", "")

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

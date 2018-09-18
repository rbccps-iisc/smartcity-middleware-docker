#!/usr/bin/env python2
import sys
import os
import time
VERSION = '0.0-1'
# No ideam.conf in /etc/ideam if during development
if os.path.exists("/etc/ideam/ideam.conf"):
    sys.path.append("/usr/share/ideam")
    os.chdir("/usr/share/ideam")

import modules.start as container_start
import modules.install as container_setup
import modules.setup as setup
import modules.generate_password as password
from datetime import datetime
from modules.utils import setup_logging
import argparse
import subprocess
from modules.utils import output_ok, output_error
import traceback
import json


class MyParser(argparse.ArgumentParser):
    """ HACK: Display a help message than just a failure message, if user types wrong arguments. """
    def error(self, message):
        sys.stderr.write('error: %s\n\n' % message)
        self.print_help()
        sys.exit(2)


def install(arguments):
    """ Installs docker images and containers."""
    setup_logging(log_file=arguments.log_file)

    if arguments.limit:
        container_setup.limit_install(str(arguments.limit).split(","))

    else:
        container_setup.check_dependencies(log_file=arguments.log_file)
        container_setup.stop_containers(["apigateway","broker","ldapd","catalogue","videoserver","webserver","elasticsearch","konga"],log_file=arguments.log_file)
        container_setup.remove_containers(["apigateway","broker","ldapd","catalogue","videoserver","webserver","elasticsearch","konga"],log_file=arguments.log_file)
        container_setup.remove_volumes(["apigateway","broker","cat","elk","ldapd","webserver"],log_file=arguments.log_file)
        password.set_passwords(arguments.config_file)
        container_setup.docker_setup(log_file=arguments.log_file,config_path=arguments.config_file)
        setup.initial_setup(log_file=arguments.log_file)
        password.update_passwords(arguments.config_file)
        setup.initial_setup_cleanup(log_file=arguments.log_file)

#       cmd = "sh /setup/setup_database.sh databasequeue"
        # initial_setup.setup_database(cmd, success_msg="Created admin user ",
        #                       failure_msg="Creation of admin user failed.",
        #                       log_file=arguments.log_file,
        #                       exit_on_fail=True)

def start(arguments):

    """ Starts all docker containers. """
    setup_logging(log_file=arguments.log_file)
    container_start.start_containers(["apigateway","broker","ldapd","elasticsearch","videoserver","webserver","catalogue","konga"],arguments.log_file)
    container_start.start_volumes(["apigateway","broker","cat","elk","ldapd","webserver"],log_file=arguments.log_file)

    if arguments.limit:
        container_start.start_services(str(arguments.limit).split(","))

    else:
        container_start.start_services(["apigateway","broker","ldapd","elasticsearch","videoserver","webserver","catalogue"])

def restart(arguments):
    """ Stops and starts all docker containers. """
    if arguments.limit:
        container_setup.stop_containers([arguments.limit],log_file=arguments.log_file)
        container_start.start_services(str(arguments.limit).split(","))

    else:
        container_setup.stop_containers(["apigateway","broker","ldapd","elasticsearch","videoserver","webserver","catalogue"],log_file=arguments.log_file)  # Stops all containers
        container_start.start_services(["apigateway","broker","ldapd","elasticsearch","videoserver","webserver","catalogue"])


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def test(arguments):
    cmd = "./tests/create_entity.sh testdevice1"
    testdevice1_key = ""

    try:
        process = subprocess.check_output(cmd, shell=True)
        register = json.loads(process)
        testdevice1_key = register["apiKey"]
        output_ok("REGISTER API: Created entity testdevice1. API KEY is " + testdevice1_key)
    except:
        output_error(process,
                     error_message=traceback.format_exc())
        exit()

    cmd = "./tests/create_entity.sh testdevice2"
    testdevice2_key = ""
    try:
        process = subprocess.check_output(cmd, shell=True)
        register = json.loads(process)
        testdevice2_key = register["apiKey"]
        output_ok("REGISTER API: Created entity testdevice2. API KEY is " + testdevice2_key)
    except:
        output_error(process,
                     error_message=traceback.format_exc())
        exit()

    cmd = "./tests/follow.sh "+ testdevice2_key + " testdevice2 testdevice1"

    try:
        process = subprocess.check_output(cmd, shell=True)

        if "200 OK" in process:
            output_ok("FOLLOW API: testdevice2 made a follow request to testdevice1")
        else:
            output_error(process,
                         error_message=traceback.format_exc())

    except:
        output_error(process,
                     error_message=traceback.format_exc())
        exit()

    time.sleep(1)

    cmd = "./tests/subscribe.sh testdevice1.follow " + testdevice1_key
    try:
        process = subprocess.check_output(cmd, shell=True)
        subscribe = json.loads(process)

        if subscribe[0]["data"]["requestor"] == "testdevice2" and subscribe[0]["data"]["permission"] == "read" :
            output_ok("FOLLOW API: testdevice1 has recieved the follow request")
        else:
            output_error(process,
                             error_message=traceback.format_exc())

    except:
        output_error(process,
                     error_message=traceback.format_exc())
        exit()

    cmd = "./tests/share.sh " + testdevice1_key + " testdevice1 testdevice2"

    try:
        process = subprocess.check_output(cmd, shell=True)

        if "200 OK" in process:
            output_ok("SHARE API: testdevice1 authorised a share request to testdevice2")
        else:
            output_error(process,
                         error_message=traceback.format_exc())

    except:
        output_error(process,
        error_message=traceback.format_exc())
        exit()

    time.sleep(1)

    cmd = "./tests/subscribe.sh testdevice2.notify " + testdevice2_key

    try:
        process = subprocess.check_output(cmd, shell=True)
        subscribe = json.loads(process)

        if "Approved" in json.dumps(subscribe):
            output_ok("SHARE API: testdevice2 has recieved the share approval")
        else:
            output_error(process,
                             error_message=traceback.format_exc())

    except:
        output_error(process,
                     error_message=traceback.format_exc())
        exit()

    cmd = "./tests/bind.sh testdevice2 testdevice1.protected " + testdevice2_key

    try:
        process = subprocess.check_output(cmd, shell=True)

        if "200 OK" in process:
            output_ok("BIND API: testdevice2 has bound its queue to testdevice1.protected exchange")
        else:
            output_error(process,
                         error_message=traceback.format_exc())

    except:
        output_error(process,
                     error_message=traceback.format_exc())
        exit()


    cmd = "./tests/publish.sh testdevice1 " + testdevice1_key
    try:
        process = subprocess.check_output(cmd, shell=True)
        if "202 Accepted" in process:
            output_ok("PUBLISH API: Published message as testdevice1.")
        else:
            output_error(process,
                         error_message=traceback.format_exc())
    except:
        output_error(process,
                     error_message=traceback.format_exc())
        exit()

    time.sleep(1)

    cmd = "./tests/subscribe.sh testdevice2 " + testdevice2_key

    try:
        process = subprocess.check_output(cmd, shell=True)
        subscribe = json.loads(process)

        if "testdata" in subscribe[0]["data"]["body"]:
            output_ok("SUBSCRIBE API: testdevice2 has recieved the data published by testdevice1")
        else:
            output_error(process,
                             error_message=traceback.format_exc())

    except:
        output_error(process,
                     error_message=traceback.format_exc())
        exit()

    cmd = "./tests/unbind.sh testdevice2 testdevice1.protected " + testdevice2_key

    try:
        process = subprocess.check_output(cmd, shell=True)

        if "200 OK" in process:
            output_ok("UNBIND API: testdevice2 has unbound its queue from testdevice1.protected exchange")
        else:
            output_error(process,
                         error_message=traceback.format_exc())

    except:
        output_error(process,
                     error_message=traceback.format_exc())
        exit()

    cmd = "./tests/publish.sh testdevice1 " + testdevice1_key
    try:
        process = subprocess.check_output(cmd, shell=True)
        if "202 Accepted" in process:
            output_ok("PUBLISH API: Published message as testdevice1.")
        else:
            output_error(process,
                         error_message=traceback.format_exc())
    except:
        output_error(process,
                     error_message=traceback.format_exc())
        exit()

    time.sleep(1)

    cmd = "./tests/subscribe.sh testdevice2 " + testdevice2_key

    try:
        process = subprocess.check_output(cmd, shell=True)
        subscribe = json.loads(process)

        if not subscribe:
            output_ok("SUBSCRIBE API: testdevice2 has not recieved the data published by testdevice1")
        else:
            output_error(process,
                         error_message=traceback.format_exc())

    except:
        output_error(process,
                     error_message=traceback.format_exc())
        exit()

    cmd = "./tests/catalogue.sh testdevice1"
    try:
        process = subprocess.check_output(cmd, shell=True)
        if "testdevice1" in process:
            output_ok("CATALOGUE API: Device testdevice1 found in catalogue.")
        else:
            output_error(process,
                         error_message=traceback.format_exc())
    except:
        output_error(process,
                     error_message=traceback.format_exc())
        exit()

    cmd = "./tests/deregister.sh testdevice1"
    try:
        process = subprocess.check_output(cmd, shell=True)
        if "success" in process:
            output_ok("DEREGISTER API: Device testdevice1 removed.")
        else:
            output_error(process,
                         error_message=traceback.format_exc())
    except:
        output_error(process,
                     error_message=traceback.format_exc())
        exit()

    cmd = "sh tests/deregister.sh testdevice2"
    try:
        process = subprocess.check_output(cmd, shell=True)
        if "success" in process:
            output_ok("DEREGISTER API: Device testdevice2 removed.")
        else:
            output_error(process,
                         error_message=traceback.format_exc())
    except:
        output_error(process,
                     error_message=traceback.format_exc())
        exit()

    cmd = "./tests/catalogue.sh testdevice1"
    try:
        process = subprocess.check_output(cmd, shell=True)
        if "apitestingdashboard" not in process:
            output_ok("CATALOGUE API: Device testdevice1 not found in catalogue.")
        else:
            output_error(process,
                         error_message=traceback.format_exc())
    except:
        output_error(process,
                     error_message=traceback.format_exc())
        exit()


def remove(arguments):
    subprocess.check_output("find {} -mindepth 3 -delete".format(arguments.rm_data_path), shell=True)

if __name__ == '__main__':
    default_log_file = "/tmp/" + datetime.now().strftime("ideam-%Y-%m-%d-%H-%M.log")
    parser = MyParser()
    subparsers = parser.add_subparsers(dest='command')

    # install command
    install_parser = subparsers.add_parser('install',
                                           description="Installs all the required docker containers for the middleware",
                                           help='Fresh installation of all the docker containers for the middleware')
    install_parser.add_argument("-l", "--limit",
                                help="Limits the ansible installation to the servers mentioned. A comma separated list"
                                     " of servers like --limit apigateway,broker",
                                required=False,
                                default="")

    # This requires sudo permission and further installation happens as root which is not desired.
    # TODO: Delete data directories (which require root privileges) and let installation be run as normal user.
    # install_parser.add_argument("-r", "--remove", type=str2bool, nargs='?', const=True,
    #                             help="Removes all the previous contents in the data directory. "
    #                                  "Passing -r will delete the data directories and if not then"
    #                                  " the data wont be deleted. Data directories are mentioned in the"
    #                                  " /etc/ideam/ideam.conf file.")
    # install_parser.add_argument("-d", "--rm-data-path",
    #                             help="Specify data directory in this argument if its not in /var/ideam/data. "
    #                                  "Default data directories are mentioned in the /etc/ideam/ideam.conf file.",
    #                             default="/var/ideam/data")

    install_parser.add_argument("-f", "--config-file",
                                help="Path to the conf file. See /etc/ideam/ideam.conf for an example.",
                                default="/etc/ideam/ideam.conf")
    install_parser.add_argument("--log-file", help="Path to log file",
                                default=default_log_file)

    # start command
    start_parser = subparsers.add_parser('start', help='Start all the docker containers in the middleware')
    start_parser.add_argument("-l",
                              "--limit",
                              help="Limits the ansible installation to the servers mentioned. A comma separated list"
                                   " of servers like --limit apigateway,broker",
                              required=False,
                              default="")
    start_parser.add_argument("--log-file", help="Path to log file",
                              default=default_log_file)

    start_parser.add_argument("--with-idps",help="Include IDPS installation after starting IDEAM or any of its components", action="store_true")

    # restart command
    restart_parser = subparsers.add_parser('restart', help='Restart all the docker containers in the middleware')
    restart_parser.add_argument("--log-file", help="Path to log file",
                                default=default_log_file)
    # remove data command
    remove_parser = subparsers.add_parser('rmdata', help='Remove all contents in the data directory')
    remove_parser.add_argument("-d", "--rm-data-path",
                                help="Path to data directory. Installation using deb file will have /var/ideam/data as"
                                     "directory. See /etc/ideam/ideam.conf for an details on data directory.",
                                default="/var/ideam/data")
    test_parser = subparsers.add_parser('test', help='Test all API endpoints')

    args = parser.parse_args()

    if args.command == "install":
        install(args)
    elif args.command == "start":
        start(args)
    elif args.command == "restart":
        start(args)
    elif args.command == "rmdata":
        remove(args)
    elif args.command == "test":
        test(args)

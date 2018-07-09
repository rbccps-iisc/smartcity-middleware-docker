#!/usr/bin/env python2
import sys
import os
VERSION = '0.0-1'
# No ideam.conf in /etc/ideam if during development
if os.path.exists("/etc/ideam/ideam.conf"):
    sys.path.append("/usr/share/ideam")
    os.chdir("/usr/share/ideam")
import modules.download_packages as download_packages
import modules.start as container_start
import modules.install as container_setup
import modules.quick_install as quick_setup
from modules.generate_password import set_passwords
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
    if arguments.limit:

        if arguments.quick:
            quick_setup.limit_install(arguments.limit)
        else:
            container_setup.ansible_installation(arguments.limit)
    else:
        setup_logging(log_file=arguments.log_file)
        container_setup.check_dependencies(log_file=arguments.log_file)

        if not arguments.quick:
            container_setup.stop_containers(log_file=arguments.log_file)
            container_setup.remove_containers(log_file=arguments.log_file)

        else:
            quick_setup.stop_containers(log_file=arguments.log_file)
            quick_setup.remove_containers(log_file=arguments.log_file)

        if not arguments.quick:
            download_packages.download(arguments.log_file)

        set_passwords(arguments.config_file)

        if arguments.quick:
            quick_setup.docker_setup(log_file=arguments.log_file,config_path=arguments.config_file)
        else:
            container_setup.docker_setup(log_file=arguments.log_file, config_path=arguments.config_file)
            subprocess.call('ansible-playbook -i hosts install.yaml '
                        '--limit "kong, rabbitmq, elasticsearch, apt_repo, tomcat, ldapd,'
                        ' hypercat, videoserver, pushpin"', shell=True)


def start(arguments):
    """ Starts all docker containers. """
    if arguments.limit:
        container_start.ansible_start(arguments.limit)
        if arguments.with_idps:
            container_start.start_idps()

    elif arguments.with_idps:
        container_start.start_all()
        container_start.start_idps()

    else:
        container_start.start_all()


def restart(arguments):
    """ Stops and starts all docker containers. """
    if arguments.limit:
        container_setup.stop_containers(log_file=arguments.log_file)
        container_start.ansible_start(arguments.limit)

    else:
        container_setup.stop_containers(log_file=arguments.log_file)  # Stops all containers
        container_start.start_all()


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def test(arguments):
    cmd = "./tests/create_entity.sh apitestingstreetlight"
    api_testing_streetlight_key = ""

    try:
        process = subprocess.check_output(cmd, shell=True)
        register = json.loads(process)
        api_testing_streetlight_key = register["apiKey"]
        output_ok("REGISTER API: Created entity apitestingstreetlight. API KEY is " + api_testing_streetlight_key)
    except:
        output_error(process,
                     error_message=traceback.format_exc())
        # f=open("/tmp/status")
        # print("File contents:" + f.read())
        # f.close()
        exit()

    cmd = "./tests/create_entity.sh apitestingdashboard"
    api_testing_dashboard_key = ""
    try:
        process = subprocess.check_output(cmd, shell=True)
        register = json.loads(process)
        api_testing_dashboard_key = register["apiKey"]
        output_ok("REGISTER API: Created entity apitestingdashboard. API KEY is " + api_testing_dashboard_key)
    except:
        output_error(process,
                     error_message=traceback.format_exc())
        exit()

    cmd = "./tests/publish.sh " + api_testing_streetlight_key
    try:
        process = subprocess.check_output(cmd, shell=True)
        if "Publish message OK" in process:
            output_ok("PUBLISH API: Published message as apitestingstreetlight.")
        else:
            output_error(process,
                         error_message=traceback.format_exc())
    except:
        output_error(process,
                     error_message=traceback.format_exc())
        exit()

    cmd = "./tests/catalogue.sh apitestingdashboard"
    try:
        process = subprocess.check_output(cmd, shell=True)
        if "apitestingdashboard" in process:
            output_ok("CATALOGUE API: Device apitestingdashboard found in catalogue.")
        else:
            output_error(process,
                         error_message=traceback.format_exc())
    except:
        output_error(process,
                     error_message=traceback.format_exc())
        exit()

    cmd = "./tests/deregister.sh"
    try:
        process = subprocess.check_output(cmd, shell=True)
        if "success" in process:
            output_ok("DEREGISTER API: Device apitestingdashboard removed.")
        else:
            output_error(process,
                         error_message=traceback.format_exc())
    except:
        output_error(process,
                     error_message=traceback.format_exc())
        exit()

    cmd = "sh tests/deregister1.sh"
    try:
        process = subprocess.check_output(cmd, shell=True)
        if "success" in process:
            output_ok("DEREGISTER API: Device apitestingstreetlight removed.")
        else:
            output_error(process,
                         error_message=traceback.format_exc())
    except:
        output_error(process,
                     error_message=traceback.format_exc())
        exit()

    cmd = "./tests/catalogue.sh apitestingdashboard"
    try:
        process = subprocess.check_output(cmd, shell=True)
        if "apitestingdashboard" not in process:
            output_ok("CATALOGUE API: Device apitestingdashboard not found in catalogue.")
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
                                     " of servers like --limit kong,rabbitmq",
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

    install_parser.add_argument("--quick",help="Use Alpine base images for quick installation of IDEAM", action="store_true")
    # start command
    start_parser = subparsers.add_parser('start', help='Start all the docker containers in the middleware')
    start_parser.add_argument("-l",
                              "--limit",
                              help="Limits the ansible installation to the servers mentioned. A comma separated list"
                                   " of servers like --limit kong,rabbitmq",
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

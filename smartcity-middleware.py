import modules.download_packages as download_packages
import modules.start as container_start
import modules.install as container_setup
from datetime import datetime
from modules.utils import setup_logging
import sys
import argparse


class MyParser(argparse.ArgumentParser):
    """ HACK: Display a help message than just a failure message, if user types wrong arguments. """
    def error(self, message):
        sys.stderr.write('error: %s\n\n' % message)
        self.print_help()
        sys.exit(2)


def install(arguments):
    """ Installs docker images and containers."""
    if args.limit:
        container_setup.ansible_setup(arguments.limit)
    else:
        setup_logging(log_file=arguments.log_file)
        container_setup.check_dependencies(log_file=arguments.log_file)
        container_setup.stop_containers(log_file=arguments.log_file)
        container_setup.remove_containers(log_file=arguments.log_file)
        download_packages.download(arguments.log_file)
        container_setup.docker_setup(log_file=arguments.log_file, config_path=arguments.config_file)
        # TODO: RabbitMQ, Catalogue fails due to network issues. Temporary fix is to run the setup again
        #       limiting the installation only to RabbitMQ and catalogue
        #       python smartcity-middleware.py -l hypercat,rabbitmq -f middleware.conf
        container_setup.ansible_setup("kong, rabbitmq, elasticsearch, apt_repo, tomcat")


def start(arguments):
    """ Starts all docker containers. """
    if arguments.limit:
        container_start.ansible_setup(arguments.limit)
    else:
        container_start.start_all()


def restart(arguments):
    """ Stops and starts all docker containers. """
    if arguments.limit:
        container_start.ansible_setup(arguments.limit)
    else:
        container_setup.stop_containers(log_file=arguments.log_file)  # Stops all containers
        container_start.start_all()


if __name__ == '__main__':
    default_log_file = "/tmp/" + datetime.now().strftime("smartcity-middleware-%Y-%m-%d-%H-%M.log")
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
    install_parser.add_argument("--log-file", help="Path to log file",
                                default=default_log_file)
    install_parser.add_argument("-f", "--config-file",
                                help="Path to the conf file. See middleware.conf for an example.",
                                required=True)

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
    # restart command
    restart_parser = subparsers.add_parser('restart', help='Restart all the docker containers in the middleware')
    restart_parser.add_argument("--log-file", help="Path to log file",
                                default=default_log_file)
    # TODO: test all APIs
    test_parser = subparsers.add_parser('test', help='Test /register, /publish, /subscribe API\'s ')
    test_parser.add_argument("--log-file", help="Path to log file",
                             default=default_log_file)

    args = parser.parse_args()

    if args.command == "install":
        install(args)
    elif args.command == "start":
        start(args)
    elif args.command == "restart":
        restart(args)

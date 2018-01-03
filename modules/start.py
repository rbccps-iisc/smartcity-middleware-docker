import subprocess
from create_hosts import create_hosts


def start_all():
    """ Starts all docker containers, OpenBSD vagrant files. """
    create_hosts()
    subprocess.call("docker start konga", shell=True)
    subprocess.call('ansible-playbook -i hosts start.yaml', shell=True)


def ansible_start(limit=""):
    create_hosts()
    subprocess.call('ansible-playbook -i hosts start.yaml --limit "' + limit + '"', shell=True)

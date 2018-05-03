import subprocess,os
from create_hosts import create_hosts


def start_all():
    """ Starts all docker containers """
    create_hosts()
    subprocess.call("docker start konga", shell=True)
    subprocess.call('ansible-playbook -i hosts start.yaml', shell=True)

def ansible_start(limit=""):
    create_hosts()
    subprocess.call('ansible-playbook -i hosts start.yaml --limit "' + limit + '"', shell=True)

def start_idps():
    if os.getlogin() == 'travis':
        subprocess.call('ansible-playbook -i \'localhost\' -s install_idps_travis.yml', shell=True)
    else:
        subprocess.call('ansible-playbook -i \'localhost\' -s install_idps.yml --ask-sudo-pass',shell=True)

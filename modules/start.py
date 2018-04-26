import subprocess,os
from create_hosts import create_hosts


def start_all():
    """ Starts all docker containers, OpenBSD vagrant files. """
    create_hosts()
    subprocess.call("docker start konga", shell=True)
    subprocess.call('ansible-playbook -i hosts start.yaml', shell=True)

    if os.getlogin() == 'travis':
        subprocess.call('ansible-playbook -i \'localhost\' -s install_idps_travis.yml', shell=True)
    else:
        subprocess.call('ansible-playbook -i \'localhost\' -s install_idps.yml --ask-sudo-pass',shell=True)


def ansible_start(limit=""):
    create_hosts()
    subprocess.call('ansible-playbook -i hosts start.yaml --limit "' + limit + '"', shell=True)

    if os.getlogin() == 'travis':
        subprocess.call('ansible-playbook -i \'localhost\' -s install_idps_travis.yml', shell=True)
    else:
        subprocess.call('ansible-playbook -i \'localhost\' -s install_idps.yml --ask-sudo-pass',shell=True)

import subprocess


def get_port(server):
    return subprocess.check_output(['docker',
                                    'inspect',
                                    """--format='{{(index (index .NetworkSettings.Ports "22/tcp") 0).HostPort}}'""",
                                    server])


def create_hosts():
    hosts = ""
    subprocess.call("docker start kong", shell=True)
    hosts += "kong ansible_host=localhost ansible_port={0} ansible_user=root\n".format(get_port("kong").rstrip())
    subprocess.call("docker start hypercat", shell=True)
    hosts += "hypercat ansible_host=localhost ansible_port={0} ansible_user=root\n".format(
        get_port("hypercat").rstrip())
    subprocess.call("docker start apt_repo", shell=True)
    hosts += "apt_repo ansible_host=localhost ansible_port={0} ansible_user=root\n".format(
        get_port("apt_repo").rstrip())
    subprocess.call("docker start elasticsearch", shell=True)
    hosts += "elasticsearch ansible_host=localhost ansible_port={0} ansible_user=root\n".format(
        get_port("elasticsearch").rstrip())
    subprocess.call("docker start ldapd", shell=True)
    hosts += "ldapd ansible_host=localhost ansible_port={0} ansible_user=root\n".format(
        get_port("ldapd").rstrip())
    subprocess.call("docker start rabbitmq", shell=True)
    hosts += "rabbitmq ansible_host=localhost ansible_port={0} ansible_user=root\n".format(
        get_port("rabbitmq").rstrip())
    subprocess.call("docker start pushpin", shell=True)
    hosts += "pushpin ansible_host=localhost ansible_port={0} ansible_user=root\n".format(
        get_port("pushpin").rstrip())
    subprocess.call("docker start tomcat", shell=True)
    hosts += "tomcat ansible_host=localhost ansible_port={0} ansible_user=root\n".format(get_port("tomcat").rstrip())
    subprocess.call("docker start videoserver", shell=True)
    hosts += "videoserver ansible_host=localhost ansible_port={0} ansible_user=root\n".format(get_port("videoserver").rstrip())
    print hosts
    with open('hosts', 'w+') as host_file:
        host_file.write(hosts)


if __name__ == '__main__':
    create_hosts()

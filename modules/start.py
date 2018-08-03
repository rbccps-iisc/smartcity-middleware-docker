import subprocess
from utils import output_error, output_info, output_ok, output_warning
import traceback
import ConfigParser
import os
from time import time
from install import subprocess_with_print

def start_containers(list,log_file):

    for container in list:

        subprocess_with_print("docker start {0}".format(container),
                              success_msg="Started {0}".format(container),
                              failure_msg="{0} container doesn't exist. SKIPPING THIS ERROR.".format(container),
                              log_file=log_file,
                              exit_on_fail=False)

    subprocess_with_print("docker volume start ldapd-data",
                          success_msg="Removed ldapd-data volume",
                          failure_msg="Ldapd-data volume doesn't exist. SKIPPING THIS ERROR.",
                          log_file=log_file,
                          exit_on_fail=False)

def start_services(list):

    #TODO commit docker images along with start scripts

    for container in list:
        output_info("Starting {0} container".format(container))

        try:
            subprocess.call('docker cp tasks/{0}/start.sh {0}:/etc/'.format(container), shell=True)
            subprocess.call('docker exec {0} /etc/start.sh'.format(container), shell=True)
        except Exception as e:
            print(e)

        output_ok("Started {0} container".format(container))

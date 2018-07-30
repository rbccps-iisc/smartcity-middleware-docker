import subprocess
from utils import output_error, output_info, output_ok, output_warning
import traceback
import ConfigParser
import os
from time import time
from install import subprocess_with_print

def start_containers(log_file):

    subprocess_with_print("docker start kong",
                          success_msg="Started Kong",
                          failure_msg="Kong container doesn't exist. SKIPPING THIS ERROR.",
                          log_file=log_file,
                          exit_on_fail=False)

    subprocess_with_print("docker start videoserver",
                          success_msg="Started Videoserver",
                          failure_msg="Videoserver container doesn't exist. SKIPPING THIS ERROR.",
                          log_file=log_file,
                          exit_on_fail=False)

    subprocess_with_print("docker start rabbitmq",
                          success_msg="Started RabbitMQ",
                          failure_msg="RabbitMQ container doesn't exist. SKIPPING THIS ERROR.",
                          log_file=log_file,
                          exit_on_fail=False)

    subprocess_with_print("docker start catalogue",
                          success_msg="Started Catalogue server",
                          failure_msg="Catalogue server container doesn't exist. SKIPPING THIS ERROR.",
                          log_file=log_file,
                          exit_on_fail=False)

    subprocess_with_print("docker start elasticsearch",
                          success_msg="Started Elasticsearch",
                          failure_msg="Elasticsearch container doesn't exist. SKIPPING THIS ERROR.",
                          log_file=log_file,
                          exit_on_fail=False)

    subprocess_with_print("docker start tomcat",
                          success_msg="Started Tomcat",
                          failure_msg="Tomcat container doesn't exist. SKIPPING THIS ERROR.",
                          log_file=log_file,
                          exit_on_fail=False)

    subprocess_with_print("docker start ldapd",
                          success_msg="Started Ldapd",
                          failure_msg="Ldapd container doesn't exist. SKIPPING THIS ERROR.",
                          log_file=log_file,
                          exit_on_fail=False)

    subprocess_with_print("docker volume start ldapd-data",
                          success_msg="Removed ldapd-data volume",
                          failure_msg="Ldapd-data volume doesn't exist. SKIPPING THIS ERROR.",
                          log_file=log_file,
                          exit_on_fail=False)

def start_services():

    print("")  # Just to separate out the individual start scripts
    output_info("Starting Kong container")

    try:
        subprocess.call('docker cp tasks/kong/quick_start_kong.sh kong:/etc/', shell=True)
        subprocess.call('docker exec kong /etc/quick_start_kong.sh', shell=True)
    except Exception as e:
        print(e)

    output_ok("Started Kong container")

    print("")

    output_info("Starting RabbitMQ container")

    try:
        subprocess.call('docker cp tasks/rabbitmq/quick_start_rmq.sh rabbitmq:/etc/', shell=True)
        subprocess.call('docker exec rabbitmq /etc/quick_start_rmq.sh', shell=True)
    except Exception as e:
        print(e)

    output_ok("Started RabbitMQ container")

    print("")
    output_info("Starting Catalogue container")

    try:
        subprocess.call('docker cp tasks/catalogue/quick_start_catalogue.sh catalogue:/etc/', shell=True)
        subprocess.call('docker exec catalogue /etc/quick_start_catalogue.sh', shell=True)
    except Exception as e:
        print(e)

    output_ok("Started Catalogue container")

    print("")
    output_info("Starting Tomcat container")

    try:
        subprocess.call('docker cp tasks/tomcat/quick_start_tomcat.sh tomcat:/etc/', shell=True)
        subprocess.call('docker exec tomcat /etc/quick_start_tomcat.sh', shell=True)
    except Exception as e:
        print(e)

    output_ok("Started Tomcat container")

    print("")
    output_info("Starting Elasticsearch container")

    try:
        subprocess.call('docker cp tasks/elasticsearch/quick_start_elk.sh elasticsearch:/etc/', shell=True)
        subprocess.call('docker exec elasticsearch /etc/quick_start_elk.sh', shell=True)
    except Exception as e:
        print(e)

    output_ok("Started Elasticsearch container")

    print("")
    output_info("Starting LDAPD container")

    try:
        subprocess.call('docker cp tasks/ldapd/quick_start_ldapd.sh ldapd:/etc/', shell=True)
        subprocess.call('docker exec ldapd /etc/quick_start_ldapd.sh', shell=True)
    except Exception as e:
        print(e)

    output_ok("Started LDAPD container")

    print("")
    output_info("Starting Videoserver container")

    try:
        subprocess.call('docker exec videoserver /etc/quick-vs-setup.sh', shell=True)
    except Exception as e:
        print(e)

    output_ok("Started Videoserver container")
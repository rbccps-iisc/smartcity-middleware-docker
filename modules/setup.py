#!/usr/bin/env python2

import subprocess
from modules.utils import output_ok, output_error, output_warning, output_info
import traceback
import json
import sys


def initial_setup(log_file):

    cmd = "docker exec apigateway mkdir /usr/local/kong/setup"
    setup_apigateway(cmd, success_msg="Created setup directory in apigateway",
                         failure_msg="Creation of setup directory in apigateway failed",
                         log_file=log_file,
                         exit_on_fail=True)

    cmd = "docker cp setup/setup_consumer.sh apigateway:/usr/local/kong/setup"
    setup_apigateway(cmd, success_msg="Copied setup_consumer.sh to setup directory",
                         failure_msg="Copying setup_consumer.sh failed",
                         log_file=log_file,
                         exit_on_fail=True)

    cmd = "docker exec apigateway chmod +x /usr/local/kong/setup/setup_consumer.sh"
    setup_apigateway(cmd, success_msg="Added necessary permissions to setup_consumer.sh",
                         failure_msg="Changing file permission failed",
                         log_file=log_file,
                         exit_on_fail=True)

    cmd = "docker cp setup/setup_consumer-acl.sh apigateway:/usr/local/kong/setup"
    setup_apigateway(cmd, success_msg="Copied setup_consumer-acl.sh to setup directory",
                         failure_msg="Copying setup_consumer-acl.sh failed",
                         log_file=log_file,
                         exit_on_fail=True)

    cmd = "docker exec apigateway chmod +x /usr/local/kong/setup/setup_consumer-acl.sh"
    setup_apigateway(cmd, success_msg="Added necessary permissions to setup_consumer-acl.sh",
                         failure_msg="Changing file permission failed",
                         log_file=log_file,
                         exit_on_fail=True)

    cmd = "docker cp setup/setup_consumer-key-auth.sh apigateway:/usr/local/kong/setup"
    setup_apigateway(cmd, success_msg="Copied setup_consumer-key-auth.sh to setup directory",
                         failure_msg="Copying setup_consumer-key-auth.sh failed",
                         log_file=log_file,
                         exit_on_fail=True)

    cmd = "docker exec apigateway chmod +x /usr/local/kong/setup/setup_consumer-key-auth.sh"
    setup_apigateway(cmd, success_msg="Added necessary permissions to setup_consumer-key-auth.sh",
                         failure_msg="Changing file permission failed",
                         log_file=log_file,
                         exit_on_fail=True)

    cmd = "docker cp setup/install.sh apigateway:/usr/local/kong/setup"
    setup_apigateway(cmd, success_msg="Copied install.sh to setup directory",
               failure_msg="Copying install.sh failed",
               log_file=log_file,
               exit_on_fail=True)

    cmd = "docker exec apigateway chmod +x /usr/local/kong/setup/install.sh"
    setup_apigateway(cmd, success_msg="Added necessary permissions to install.sh",
               failure_msg="Changing file permission failed",
               log_file=log_file,
               exit_on_fail=True)

    cmd = "docker exec apigateway /usr/local/kong/setup/install.sh"
    setup_apigateway(cmd, success_msg="Executing initial setup script",
               failure_msg="Initial setup failed",
               log_file=log_file,
               exit_on_fail=True)

    cmd = "docker cp apigateway:/usr/local/kong/auth_out.log ."
    setup_apigateway(cmd, success_msg="Copying apikey",
               failure_msg="Failed copying apikey",
               log_file=log_file,
               exit_on_fail=True)

    with open('auth_out.log') as response:
        data = json.load(response)
        apikey = data["key"]

    cmd = "docker cp setup/setup_database.sh apigateway:/usr/local/kong/setup"
    setup_apigateway(cmd, success_msg="Copied setup_database.sh to setup directory",
               failure_msg="Copying setup_database.sh failed",
               log_file=log_file,
               exit_on_fail=True)

    cmd = "docker cp setup/register_database.sh apigateway:/usr/local/kong/setup"
    setup_apigateway(cmd, success_msg="Copied register_database.sh to setup directory",
               failure_msg="Copying register_database.sh failed",
               log_file=log_file,
               exit_on_fail=True)

    cmd = "docker exec apigateway chmod +x /usr/local/kong/setup/register_database.sh"
    setup_apigateway(cmd, success_msg="Added necessary permissions to register_database.sh",
               failure_msg="Changing file permission failed",
               log_file=log_file,
               exit_on_fail=True)


    cmd = "docker exec apigateway chmod +x /usr/local/kong/setup/setup_database.sh"
    setup_apigateway(cmd, success_msg="Added necessary permissions to setup_database.sh",
               failure_msg="Changing file permission failed",
               log_file=log_file,
               exit_on_fail=True)

    cmd = "docker exec apigateway /usr/local/kong/setup/register_database.sh"
    setup_apigateway(cmd, success_msg="Executing database setup script",
               failure_msg="Database setup failed",
               log_file=log_file,
               exit_on_fail=True)

    cmd = "docker exec apigateway /usr/local/kong/setup/setup_database.sh " + apikey + " database"
    setup_apigateway(cmd, success_msg="Executing database setup script",
               failure_msg="Database setup failed",
               log_file=log_file,
               exit_on_fail=True)

    cmd = "docker cp apigateway:/usr/local/kong/setup/database_out.log ."
    setup_apigateway(cmd, success_msg="Copying database apikey",
               failure_msg="Failed copying database apikey",
               log_file=log_file,
               exit_on_fail=True)

    with open('database_out.log') as response:
        data = json.load(response)
        apikey = data["apiKey"]


    # with open("ideam.conf", "a") as text_file:
    #    text_file.write("database = {0}".format(key))
    #    output_ok("Copied database key to ideam.conf file")

    # cmd = "sh ../setup/setup_database.sh " + key + " databasequeue"
    # setup_database(cmd, success_msg="Created database user ",
    #                        failure_msg="Creation of database user failed.",
    #                        log_file=log_file,
    #                        exit_on_fail=True))

def initial_setup_cleanup(log_file):

    cmd = "docker exec apigateway rm -rf /usr/local/kong/setup"
    cleanup_setup_apigateway(cmd, success_msg="Removed setup files in apigateway",
                             info_msg="Removing setup files in apigateway",
                             failure_msg="Removing setup files in apigateway failed",
                             log_file=log_file,
                             exit_on_fail=True)

    cmd = "rm -rf auth_out.log"
    cleanup_setup_apigateway(cmd, success_msg="Removed auth_out log file in installation directory",
                             info_msg="Removing auth_out log file in installation directory",
                             failure_msg="Removing auth_out log file in installation directory",
                             log_file=log_file,
                             exit_on_fail=True)


    cmd = "rm -rf database_out.log"
    cleanup_setup_apigateway(cmd, success_msg="Removed database_out log file in installation directory",
                             info_msg="Removing database_out log file in installation directory",
                             failure_msg="Removing database_out log file in installation directory",
                             log_file=log_file,
                             exit_on_fail=True)


def setup_database(cmd, success_msg, failure_msg, log_file, exit_on_fail=False):
    """ Create a subprocess call and outputs success and errors if any.

    Args:
        cmd          (string): docker instance name
        success_msg  (string): success message to be displayed in [OK] format.
        failure_msg  (string): failure text to be displayed with [FAILED] format.
        log_file     (string): log file path
        exit_on_fail   (bool): exit program if failed
    """

    try:
        process = subprocess.check_output(cmd, shell=True)
        register = json.loads(process)
        database_key = register["apiKey"]
        output_ok("REGISTER API: Created entity database. API KEY is " + database_key)
    except:
        output_error(process,
                     error_message=traceback.format_exc())
        # f=open("/tmp/status")
        # print("File contents:" + f.read())
        # f.close()
        exit()

def setup_apigateway(cmd, success_msg, failure_msg, log_file, exit_on_fail=False):
    """ Create a subprocess call and outputs success and errors if any.

    Args:
        cmd          (string): docker instance name
        success_msg  (string): success message to be displayed in [OK] format.
        failure_msg  (string): failure text to be displayed with [FAILED] format.
        log_file     (string): log file path
        exit_on_fail   (bool): exit program if failed
    """
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


def cleanup_setup_apigateway(cmd, success_msg, info_msg, failure_msg, log_file, exit_on_fail=False):
    """ Create a subprocess call and outputs success and errors if any.

    Args:
        cmd          (string): docker instance name
        success_msg  (string): success message to be displayed in [OK] format.
        failure_msg  (string): failure text to be displayed with [FAILED] format.
        log_file     (string): log file path
        exit_on_fail   (bool): exit program if failed
    """
    try:
        process = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output_info(info_msg, message=process.stdout.read(), stderr=process.stderr.read())
        output_ok(success_msg, message=process.stdout.read(), stderr=process.stderr.read())


    except OSError:
        if exit_on_fail:
            output_error(failure_msg + "\n           Check logs {0} for more details.".format(log_file),
                         error_message=traceback.format_exc())
            exit()
        else:
            output_warning(failure_msg + "\n           Check logs {0} for more details.".format(log_file),
                           error_message=traceback.format_exc())


import string
import random
import ConfigParser
import json


def id_generator(size=16, chars=string.ascii_letters + string.digits + "_+^/"):
    return ''.join(random.choice(chars) for _ in range(size))

def ldap_pass(config):

    password = config.get('PASSWORDS', 'LDAP')

    if password == "?":
        password = id_generator(size=16, chars=string.ascii_letters + string.digits)

    write("host_vars/ldapd", "ldapd_password: " + password)
    write("config/webserver/pwd", password)

    replace("config/catalogue/config.js", "ldap_pwd", password, "config/catalogue/config_new.js")
    replace("config/ldapd/ldapd.conf", "ldap_pwd", password, "config/ldapd/ldapd_new.conf")

    config.set('PASSWORDS', 'LDAP', password)


def replace(path, old, new, new_path):

    with open(path, 'r') as f:
        data = f.read()

    data = data.replace(old, new)

    with open(new_path, 'w+') as f:
        f.write(data)

def rmq_pass(config):

    password = config.get('PASSWORDS', 'BROKER')

    if password == "?":
        password = id_generator(size=16, chars=string.ascii_letters + string.digits)

    write("config/webserver/rmqpwd", password)
    write("host_vars/broker", "password: " + password)

    replace("config/elasticsearch/logstash-input-rabbitmq.conf", "rmq_pwd", password,
            "config/elasticsearch/logstash-input-rabbitmq_new.conf")
    replace("config/elasticsearch/logstash-input-rabbitmq_new.conf", "rmq_user", "admin.ideam",
            "config/elasticsearch/logstash-input-rabbitmq_new.conf")
    
    config.set('PASSWORDS', 'BROKER', password)
  
def cdxadmin(config):
    password = config.get('PASSWORDS', 'cdx.admin')
    with open('auth_out.log') as response:
            data = json.load(response)
            key = data["key"]
    config.set('PASSWORDS', 'CDX.ADMIN', key)

def database(config):
    password = config.get('PASSWORDS', 'database')
    with open('database_out.log') as response:
            data = json.load(response)
            key = data["apiKey"]
    config.set('PASSWORDS', 'DATABASE', key)

def write(path, contents):
    with open(path, 'w+') as f:
        f.write(contents)

def set_passwords(conf):

    config = ConfigParser.ConfigParser()
    config.readfp(open(conf))
    ldap_pass(config)
    rmq_pass(config)

    with open(conf, 'w+') as configfile:
        config.write(configfile)

def update_passwords(conf):
    config = ConfigParser.ConfigParser()
    config.readfp(open(conf))
    cdxadmin(config)
    database(config)
    with open(conf, 'w+') as configfile:
        config.write(configfile)
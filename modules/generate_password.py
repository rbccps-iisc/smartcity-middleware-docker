import passlib.hash
import string
import random
import ConfigParser


def id_generator(size=16, chars=string.ascii_letters + string.digits + "_+^/"):
    return ''.join(random.choice(chars) for _ in range(size))


def ansible_user_pass(config):
    password = config.get('PASSWORDS', 'USER_ANSIBLE')
    if password == "?":
        password = id_generator()
    sha_hash = passlib.hash.sha512_crypt.encrypt(password)
    write("host_vars/all", "password: " + sha_hash)
    config.set('PASSWORDS', 'USER_ANSIBLE', password)


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


def kong_pass(config):
    password = config.get('PASSWORDS', 'APIGATEWAY')
    if password == "?":
        password = id_generator()
    write("host_vars/apigateway", "kong_password: " + password + "\npostgresql_password: " + password)
    with open('config/apigateway/kong.conf', 'r') as f:
        data = f.read()
    data = data + "\npg_password = " + str(password)
    with open('config/apigateway/kong_new.conf', 'w+') as f:
        f.write(data)
    config.set('PASSWORDS', 'APIGATEWAY', password)


def catalogue_pass(config):
    password = config.get('PASSWORDS', 'catalogue')
    if password == "?":
        password = id_generator()
    write("host_vars/catalogue", "mongodb_password: " + password)
    config.set('PASSWORDS', 'catalogue', password)


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
    # replace("config/kong/share_new.py", "rmq_pwd", password, "config/kong/share_new.py")
    # replace("config/kong/share_new.py", "rmq_user", "admin.ideam", "config/kong/share_new.py")
    config.set('PASSWORDS', 'BROKER', password)


def idps_pass(config):
    password = config.get('PASSWORDS', 'IDPS')
    if password == "?":
        password = id_generator()
    write("host_vars/idps", "db_password: " + password)
    config.set('PASSWORDS', 'IDPS', password)


def write(path, contents):
    with open(path, 'w+') as f:
        f.write(contents)


def set_passwords(conf):
    config = ConfigParser.ConfigParser()
    config.readfp(open(conf))
    ansible_user_pass(config)
    ldap_pass(config)
    kong_pass(config)
    catalogue_pass(config)
    idps_pass(config)
    rmq_pass(config)
    with open(conf, 'w+') as configfile:
        config.write(configfile)

import passlib.hash
import string
import random
import ConfigParser
passwords = dict()


def id_generator(size=16, chars=string.ascii_letters + string.digits + "_-+@.:^!?/\\"):
    return ''.join(random.choice(chars) for _ in range(size))


def ansible_user_pass(config):
    password = config.get('PASSWORDS', 'USER_ANSIBLE')
    if password == "??????":
        password = id_generator()
    sha_hash = passlib.hash.sha512_crypt.encrypt(password)
    write("host_vars/all", "password: " + sha_hash)
    passwords["ansible"] = password
    config.set('PASSWORDS', 'USER_ANSIBLE', password)


def ldap_pass(config):
    password = config.get('PASSWORDS', 'LDAP')
    if password == "??????":
        password = id_generator()
    write("host_vars/ldapd", "ldapd_password: " + password)
    write("config/tomcat/pwd", password)
    replace("config/hypercat/config.js", "secret0", password, "config/hypercat/config_new.js")
    replace("config/ldapd/ldapd.conf", "secret0", password, "config/ldapd/ldapd_new.conf")
    replace("config/kong/share.py", "secret0", password, "config/kong/share_new.py")
    passwords["ldapd"] = password
    config.set('PASSWORDS', 'LDAP', password)


def replace(path, old, new, new_path):
    with open(path, 'r') as f:
        data = f.read()
    data = data.replace(old, new)
    with open(new_path, 'w+') as f:
        f.write(data)


def kong_pass(config):
    password = config.get('PASSWORDS', 'KONG')
    if password == "??????":
        password = id_generator()
    write("host_vars/kong", "kong_password: " + password + "\npostgresql_password: " + password)
    passwords["kong"] = password
    with open('config/kong/kong.conf', 'r') as f:
        data = f.read()
    data = data + "\npg_password = " + str(passwords["kong"])
    with open('config/kong/kong_new.conf', 'w+') as f:
        f.write(data)
    config.set('PASSWORDS', 'KONG', password)


def catalogue_pass(config):
    password = config.get('PASSWORDS', 'HYPERCAT')
    if password == "??????":
        password = id_generator()
    write("host_vars/hypercat", "mongodb_password: " + password)
    passwords["hypercat"] = password
    config.set('PASSWORDS', 'HYPERCAT', password)


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
    with open(conf, 'w+') as configfile:
        config.write(configfile)

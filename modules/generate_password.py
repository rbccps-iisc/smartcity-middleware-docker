import passlib.hash
import string
import random
import ConfigParser
passwords = dict()


def id_generator(size=15, chars=string.ascii_letters + string.digits + "@#$%&"):
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
    passwords["ldapd"] = password
    config.set('PASSWORDS', 'LDAP', password)


def kong_pass(config):
    password = config.get('PASSWORDS', 'KONG')
    if password == "??????":
        password = id_generator()
    write("host_vars/kong", "kong_password: " + password + "\npostgresql_password: "+password)
    passwords["kong"] = password
    with open('config/kong/kong.conf', 'a') as f:
        f.write("pg_password = " + str(password["kong"]))
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
    with open('middleware.conf', 'w+') as configfile:
        config.write(configfile)

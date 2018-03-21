import passlib.hash
import string
import random
import ConfigParser


passwords = dict()


def id_generator(size=15, chars=string.ascii_letters + string.digits + "!@#$%&"):
    return ''.join(random.choice(chars) for _ in range(size))


def ansible_user_account(conf):
    config = ConfigParser.ConfigParser()
    config.readfp(open(conf))
    password = config.get('PASSWORDS', 'USER_ANSIBLE')
    if password == "??????":
        password = id_generator()
    sha_hash = passlib.hash.sha512_crypt.encrypt(password)
    write("host_vars/all", "password: " + sha_hash)
    passwords["ansible"] = password
    config.set('PASSWORDS', 'USER_ANSIBLE', 'ansible')
    with open('middleware.conf', 'w') as configfile:
        config.write(configfile)


def write(file, contents):
    with open(file, 'w') as f:
        f.write(contents)

import subprocess
import json
import ConfigParser

register = subprocess.check_output("./tests/create_entity.sh streetlight", shell=True)
print(register)
register = json.loads(register)
streetlight_key = register["apiKey"]
print(streetlight_key)
register = subprocess.check_output("./tests/create_entity.sh dashboard", shell=True)
print(register)
register = json.loads(register)
dashboard_key = register["apiKey"]
print(dashboard_key)
publish = subprocess.check_output("./tests/publish.sh "+streetlight_key, shell=True)
print(publish)
config = ConfigParser.ConfigParser()
config.readfp(open("ideam.conf"))
password = config.get('PASSWORDS', 'USER_ANSIBLE')
sshtest = subprocess.check_output("./tests/ssh_test.sh "+password, shell=True)
print(sshtest)
deregister = subprocess.check_output("./tests/deregister.sh", shell=True)
print(deregister)
db = subprocess.check_output("./tests/database.sh " + streetlight_key, shell=True)
print(db)

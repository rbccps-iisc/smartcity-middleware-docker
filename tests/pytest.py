import subprocess
import json

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

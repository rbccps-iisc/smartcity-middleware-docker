from datetime import datetime
import json
import requests
import subprocess
import re
import time
import sys

consumers_list=[]
ldap_ip=""
kong_ip=""
ldap_password=""
ideam_home=str(sys.argv[1])

def delete_share_entry(desc,uid):

    global ldap_password,ldap_ip

    cmd1 = "ldapdelete -H ldap://"+ldap_ip+":8389 -D \"cn=admin,dc=smartcity\" -w "+ldap_password
    cmd2 = """ "description={0},description=share,description=broker,uid={1},cn=devices,dc=smartcity" -r""". \
        format(desc,uid)
    cmd = cmd1 + cmd2
    try:
        resp = subprocess.check_output(cmd, shell=True)
        print("Deleted "+desc+" share entry in device "+uid)
    except subprocess.CalledProcessError as e:
        print(e)

def check_entity_exists(uid):

    global ldap_ip,ldap_password

    cmd1 = "ldapsearch -H ldap://"+ldap_ip+":8389 -D \"cn=admin,dc=smartcity\" -w "+ldap_password+" -b"
    cmd2 = """ "uid={0},cn=devices,dc=smartcity" """.\
        format(uid)
    cmd = cmd1 + cmd2
    resp = b""
    try:
        resp = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(e)
    check = "result: 0 Success"
    a = bytes(check, 'utf8') in resp
    return a

def check_expiry(uid):

    global ldap_password,ldap_ip

    cmd1 = "ldapsearch -H ldap://"+ldap_ip+":8389 -D \"cn=admin,dc=smartcity\" -w "+ldap_password+" -b"
    cmd2 = """ "description=share,description=broker,uid={0},cn=devices,dc=smartcity" """. \
        format(uid)
    cmd = cmd1 + cmd2
    resp=""

    try:
        resp = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(e)

    p = re.compile("validity: (.*)")
    resp=resp.decode('utf-8')
    resp=resp.split("\n")
    i=0
    for entry in resp:
        if p.match(entry):
            desc=resp[i-3].split(":")[1].strip()
            date=p.findall(entry)
            date=''.join(date)
            now=datetime.now().timestamp()

            try:
                if now>float(date):
                    delete_share_entry(desc,uid)
            except:
                pass

        i+=1

def get_ips():

    global ldap_ip, kong_ip

    resp = ""

    try:
        resp = subprocess.check_output("docker network inspect mynet", shell=True)
    except Exception as e:
        print(e)

    data = json.loads(resp.decode("utf-8").replace("\'", "\""))
    data = json.dumps(data)[1:-1]
    data = json.loads(data)

    for entry in data['Containers']:

        if data["Containers"][entry]["Name"] == "ldapd":
            ldap_ip = str(data["Containers"][entry]["IPv4Address"]).split("/")[0]

        if data["Containers"][entry]["Name"] == "kong":
            kong_ip = str(data["Containers"][entry]["IPv4Address"]).split("/")[0]

    if ldap_ip == "" or kong_ip == "":
        print("Please start all docker containers")
        exit(code=1)

def read_pwd():
    global ideam_home,ldap_password
    f=open(ideam_home+"/host_vars/ldapd","r")
    ldap_password=f.readline().split(":")[1]

def main():

    global consumers_list,kong_ip

    get_ips()
    read_pwd()

    r=requests.get("http://"+kong_ip+":8001/consumers/")
    data=json.loads(r.text)

    for entry in data['data']:
        consumers_list.append(entry['username'])

    for user in consumers_list:
        if check_entity_exists(user):
            check_expiry(user)

starttime=time.time()
while True:
  main()
  time.sleep(60.0 - ((time.time() - starttime) % 60.0))

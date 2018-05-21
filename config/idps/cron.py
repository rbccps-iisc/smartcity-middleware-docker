from datetime import datetime
import json
import requests
import subprocess
import re

consumers_list=[]

def delete_share_entry(desc,uid):
    cmd1 = """ldapdelete -H ldap://172.18.0.6:8389 -D "cn=admin,dc=smartcity" -w xRVF!Qowj-3iKWnT """
    cmd2 = """ "description={0},description=share,description=broker,uid={1},cn=devices,dc=smartcity" -r""". \
        format(desc,uid)
    cmd = cmd1 + cmd2
    try:
        resp = subprocess.check_output(cmd, shell=True)
        print("Deleted "+desc+" share entry in device "+uid)
    except subprocess.CalledProcessError as e:
        print(e)

def check_entity_exists(uid):
    cmd1 = """ldapsearch -H ldap://172.18.0.6:8389 -D "cn=admin,dc=smartcity" -w xRVF!Qowj-3iKWnT -b"""
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
    cmd1 = """ldapsearch -H ldap://172.18.0.6:8389 -D "cn=admin,dc=smartcity" -w xRVF!Qowj-3iKWnT -b"""
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

def main():

    global consumers_list

    r=requests.get("http://172.18.0.2:8001/consumers/")
    data=json.loads(r.text)

    for entry in data['data']:
        consumers_list.append(entry['username'])

    for user in consumers_list:
        if check_entity_exists(user):
            check_expiry(user)

if __name__ == '__main__':
    main()


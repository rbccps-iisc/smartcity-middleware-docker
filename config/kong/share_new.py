from japronto import Application
import json
import requests
from time import gmtime, strftime
import subprocess


def deregister(request):
    consumer_id = ""
    entity = ""
    for name, value in request.headers.items():
        if name == "X-Consumer-Username":
            consumer_id = value
    print(request.text)
    print("consumer_id     : " + str(consumer_id))
    e = json.loads(request.text)
    if "entityID" in e:
        entity = str(e["entityID"])
    print("entityID        : " + str(entity))
    if check_entity_exists(entity) is False:
        return request.Response(json={'status': 'failure',
                                      'response': "Entity doesn't exist."}, code=400)
    if check_owner(consumer_id, entity) is False:
        return request.Response(json={'status': 'failure',
                                      'response': "Only owner can remove an entity."}, code=400)
    # TODO: remove rbccps user to provider and his apikey ( which cant be used now, as its not there in ldap)
    rabbitmq_queue_delete(entity, "rbccps", "rbccps@123")
    rabbitmq_queue_delete(entity+".follow", "rbccps", "rbccps@123")
    rabbitmq_exchange_delete(entity, "rbccps", "rbccps@123")
    rabbitmq_exchange_delete(entity+".configure", "rbccps", "rbccps@123")
    rabbitmq_exchange_delete(entity+".follow", "rbccps", "rbccps@123")
    rabbitmq_exchange_delete(entity+".public", "rbccps", "rbccps@123")
    rabbitmq_exchange_delete(entity+".protected", "rbccps", "rbccps@123")
    rabbitmq_exchange_delete(entity+".private", "rbccps", "rbccps@123")
    ldap_entity_delete(entity)
    kong_consumer_delete(entity)
    catalogue_delete(entity)
    return request.Response(json={'status': 'success',
                                  'response': entity + " entity removed. "}, code=200)


def catalogue_delete(entity):
    url = 'http://hypercat:8000/cat?id=' + entity
    headers = {'pwd': 'local123'}
    r = requests.delete(url, data=json.dumps({}), headers=headers)
    print(r.text)


def rabbitmq_queue_delete(qname, consumer_id, apikey):
    url = 'http://rabbitmq:8000/queue'
    headers = {'X-Consumer-Username': consumer_id, 'Apikey': apikey, 'Accept': 'application/json'}
    data = {'name': qname}
    r = requests.delete(url, data=json.dumps(data), headers=headers)
    print(r.text)


def kong_consumer_delete(name):
    url = 'http://kong:8001/consumers/' + name
    r = requests.delete(url)
    print(r.text)


def rabbitmq_exchange_delete(ename, consumer_id, apikey):
    url = 'http://rabbitmq:8000/exchange'
    headers = {'X-Consumer-Username': consumer_id, 'Apikey': apikey, 'Accept': 'application/json'}
    data = {'name': ename}
    r = requests.delete(url, data=json.dumps(data), headers=headers)
    print(r.text)


def ldap_entity_delete(uid):
    cmd1 = """ldapdelete -H ldap://ldapd:8389 -D "cn=admin,dc=smartcity" -w xRVF!Qowj-3iKWnT """
    cmd2 = """ "uid={0},cn=devices,dc=smartcity" -r""".\
        format(uid)
    cmd = cmd1 + cmd2
    try:
        resp = subprocess.check_output(cmd, shell=True)
        print(resp)
    except subprocess.CalledProcessError as e:
        print(e)


def check_entity_exists(uid):
    cmd1 = """ldapsearch -H ldap://ldapd:8389 -D "cn=admin,dc=smartcity" -w xRVF!Qowj-3iKWnT -b"""
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
    print("check_entity_exists: " + str(a))
    return a


def check_owner(owner, device):
    cmd1 = """ldapsearch -H ldap://ldapd:8389 -D "cn=admin,dc=smartcity" -w xRVF!Qowj-3iKWnT -b"""
    cmd2 = """ "uid={0},cn=devices,dc=smartcity" {1}""".\
        format(device, "owner")
    cmd = cmd1 + cmd2
    resp = b""
    try:
        resp = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(e)
    if str(owner) == "":
        return False
    check = "owner: " + owner
    a = bytes(check, 'utf8') in resp
    print("check_owner :" + str(a))
    return a


def follow(request):
    consumer_id = ""
    apikey = ""
    for name, value in request.headers.items():
        if name == "X-Consumer-Username":
            consumer_id = value
        elif name == "Apikey":
            apikey = value
    print(request.text)
    print("consumer_id  : " + str(consumer_id))
    e = json.loads(request.text)
    if "entityID" in e and "permission" in e:
        entity = e["entityID"]  # TODO: check if entity exists in LDAP
        permission = e["permission"]
    else:
        return request.Response(json={'status': 'failure',
                                      'response': 'Input data not in correct format.'}, code=400)
    print("Entity       : " + str(entity))
    print("Permission   : " + str(permission))
    # Following device own exchanges
    if entity == consumer_id:
        bind(consumer_id, entity, "#", consumer_id, apikey)
        return request.Response(text=" A follow request was approved to exchange " + entity + " with " + permission +
                                     " access at " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " GMT.\n")
    elif entity == consumer_id + ".protected":
        bind(consumer_id, entity, "#", consumer_id, apikey)
        return request.Response(text=" A follow request was approved to exchange " + entity + " with " + permission +
                                     " access at " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " GMT.\n")
    elif entity == consumer_id + ".public":
        bind(consumer_id, entity, "#", consumer_id, apikey)
        return request.Response(text=" A follow request was approved to exchange " + entity + " with " + permission +
                                     " access at " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " GMT.\n")
    elif entity == consumer_id + ".configure":
        bind(consumer_id, entity, "#", consumer_id, apikey)
        return request.Response(text=" A follow request was approved to exchange " + entity + " with " + permission +
                                     " access at " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " GMT.\n")
    elif entity == consumer_id + ".private":
        bind(consumer_id, entity, "#", consumer_id, apikey)
        return request.Response(text=" A follow request was approved to exchange " + entity + " with " + permission +
                                     " access at " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " GMT.\n")
    else:
        create_queue(entity + ".follow", consumer_id, apikey)  # TODO it should be as part of RegisterAPI, must remove
        create_exchange("public", consumer_id, apikey)  # TODO it should be part of RegisterAPI
        bind(entity + ".follow", "public", entity + ".follow", consumer_id, apikey)
        print(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " Entity " + consumer_id +
              " made a follow request. Requested access is for " + permission)
        publish(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " Entity " + consumer_id +
                " made a follow request. Requested access is for " + permission, "public",
                entity + ".follow", consumer_id, apikey)
    return request.Response(text=" A follow request has been made to entity " + entity + " with " + permission +
                                 " access at " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " GMT.\n")


def create_queue(qname, consumer_id, apikey):
    url = 'http://rabbitmq:8000/queue'
    headers = {'X-Consumer-Username': consumer_id, 'Apikey': apikey, 'Accept': 'application/json'}
    data = {'name': qname, "durable": True}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print(r.text)


def create_exchange(ename, consumer_id, apikey):
    url = 'http://rabbitmq:8000/exchange'
    headers = {'X-Consumer-Username': consumer_id, 'Apikey': apikey, 'Accept': 'application/json'}
    data = {"name": ename, "type": "topic", "durable": True, "autodelete": False}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print(r.text)


def bind(queue, exchange, key, consumer_id, apikey):
    url = 'http://rabbitmq:8000/queue/bind'
    # TODO: FIX it in register API
    headers = {'X-Consumer-Username': consumer_id, 'Apikey': apikey, 'Accept': 'application/json'}
    data = {"queue": queue, "exchange": exchange, "key": [key]}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print(r.text)


def unbind(queue, exchange, key, consumer_id, apikey):
    url = 'http://rabbitmq:8000/queue/bind'
    # TODO: FIX it in register API
    headers = {'X-Consumer-Username': consumer_id, 'Apikey': apikey, 'Accept': 'application/json'}
    data = {"queue": queue, "exchange": exchange, "key": [key]}
    r = requests.delete(url, data=json.dumps(data), headers=headers)
    print(r.text)


def publish(body, exchange, key, consumer_id, apikey):
    url = 'http://rabbitmq:8000/publish'
    # TODO: FIX it in register API
    headers = {'X-Consumer-Username': consumer_id, 'Apikey': apikey, 'Accept': 'application/json'}
    data = {"exchange": exchange, "key": key, "body": body}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print(r.text)


def ldap_add_share_entry(device, consumer_id, read="false", write="false"):
    add = 'ldapadd -x -D "cn=admin,dc=smartcity" -w xRVF!Qowj-3iKWnT -f /tmp/share.ldif -H ldap://ldapd:8389'
    modify = 'ldapmodify -a -D "cn=admin,dc=smartcity" -w xRVF!Qowj-3iKWnT -f /tmp/share.ldif -H ldap://ldapd:8389'
    ldif = """dn: description={0},description=share,description=broker,uid={1},cn=devices,dc=smartcity
objectClass: broker
objectClass: exchange
objectClass: queue
objectClass: share
description: {0}
read: {2}
write: {3}""".format(device, consumer_id, read, write)
    f = open('/tmp/share.ldif', 'w')
    f.write(ldif)
    f.close()
    try:
        resp = subprocess.check_output(add, shell=True)
        print(resp)
    except subprocess.CalledProcessError as e:
        if str(e)[-2:] == "80" or str(e)[-2:] == "68":  # already exists
            ldif = """dn: description={0},description=share,description=broker,uid={1},cn=devices,dc=smartcity
changetype: modify
replace: read
read: {2}
-
replace: write
write: {3}""".format(device, consumer_id, read, write)
            f = open('/tmp/share.ldif', 'w')
            f.write(ldif)
            f.close()
            resp = subprocess.check_output(modify, shell=True)
            print(resp)


def ldap_add_exchange_entry(device, consumer_id, read="false", write="false"):
    add = 'ldapadd -x -D "cn=admin,dc=smartcity" -w xRVF!Qowj-3iKWnT -f /tmp/exchange.ldif -H ldap://ldapd:8389'
    modify = 'ldapmodify -a -D "cn=admin,dc=smartcity" -w xRVF!Qowj-3iKWnT -f /tmp/exchange.ldif -H ldap://ldapd:8389'
    ldif = """dn: description={0},description=exchange,description=broker,uid={1},cn=devices,dc=smartcity
objectClass: broker
objectClass: exchange
objectClass: queue
objectClass: share
description: {0}
read: {2}
write: {3}""".format(device, consumer_id, read, write)
    f = open('/tmp/exchange.ldif', 'w')
    f.write(ldif)
    f.close()
    try:
        resp = subprocess.check_output(add, shell=True)
        print(resp)
    except subprocess.CalledProcessError as e:
        if str(e)[-2:] == "80" or str(e)[-2:] == "68":  # already exists
            ldif = """dn: description={0},description=exchange,description=broker,uid={1},cn=devices,dc=smartcity
changetype: modify
replace: read
read: {2}
-
replace: write
write: {3}""".format(device, consumer_id, read, write)
            f = open('/tmp/exchange.ldif', 'w')
            f.write(ldif)
            f.close()
            resp = subprocess.check_output(modify, shell=True)
            print(resp)


def share(request):
    consumer_id = ""
    apikey = ""
    for name, value in request.headers.items():
        if name == "X-Consumer-Username":
            consumer_id = value
        elif name == "Apikey":
            apikey = value
    print(request.text)
    print("consumer_id  : " + str(consumer_id))
    e = json.loads(request.text)
    if "entityID" in e and "permission" in e:
        entity = e["entityID"]  # TODO: check if entity exists in LDAP
        permission = e["permission"]
    else:
        return request.Response(json={'status': 'failure',
                                      'response': 'Input data not in correct format.'}, code=400)
    # exchange applicable for write permission only.
    if "exchange" in e:
        exchange = e["exchange"]
    else:
        exchange = consumer_id + ".protected"

    print("Permission   : " + str(permission))
    print("shareToEntity: " + str(entity))
    print("exchange applicable for write permission only.")
    print("exchange     : " + str(exchange))

    if permission == "read" or permission == "write" or permission == "read-write":
        pass
    else:
        return request.Response(json={'status': 'failure',
                                      'response': 'permission field not in correct format.'}, code=400)
    if permission == "read":
        # This ldap_add_share_entry provides a list of people who subscribed.
        if check_ldap_entry(entity, consumer_id, "write", "true"):
            ldap_add_share_entry(entity, consumer_id, read="true", write="true")
        else:
            ldap_add_share_entry(entity, consumer_id, read="true", write="false")
        bind(entity, consumer_id + ".protected", "#", consumer_id, apikey)
        text = "Read access given to " + entity + " at " + consumer_id + " exchange.\n"
        return request.Response(text=text)
    elif permission == "write":
        if check_ldap_entry(entity, consumer_id, "read", "true"):
            ldap_add_share_entry(entity, consumer_id, read="true", write="true")
        else:
            ldap_add_share_entry(entity, consumer_id, read="false", write="true")
        ldap_add_exchange_entry(exchange, entity, read="false", write="true")
        text = "Write access given to " + entity + " at " + exchange + " exchange.\n"
        return request.Response(text=text)
    elif permission == "read-write":
        ldap_add_share_entry(entity, consumer_id, read="true", write="true")
        bind(entity, consumer_id + ".protected", "#", consumer_id, apikey)
        ldap_add_exchange_entry(exchange, entity, read="false", write="true")
        text = "Read access given to " + entity + " at " + consumer_id + " exchange.\n"
        text += "Write access given to " + entity + " at " + exchange + " exchange.\n"
        return request.Response(text=text)

    return request.Response(text="share success\n")


def unfollow(request):
    consumer_id = ""
    apikey = ""
    for name, value in request.headers.items():
        if name == "X-Consumer-Username":
            consumer_id = value
        elif name == "Apikey":
            apikey = value
    print(request.text)
    print("consumer_id     : " + str(consumer_id))
    e = json.loads(request.text)
    if "entityID" in e and "permission" in e:
        entity = e["entityID"]  # TODO: check if entity exists in LDAP
        permission = e["permission"]
    else:
        return request.Response(json={'status': 'failure',
                                      'response': 'Input data not in correct format.'}, code=400)

    # exchange applicable for write permission only.
    if "exchange" in e:
        exchange = e["exchange"]
    else:
        exchange = consumer_id + ".protected"

    print("Permission      : " + str(permission))
    print("unfollow Entity : " + str(entity))
    print("exchange applicable for write permission only.")
    print("exchange        : " + str(exchange))

    if permission == "read" or permission == "write" or permission == "read-write":
        pass
    else:
        return request.Response(json={'status': 'failure',
                                      'response': 'permission field not in correct format.'}, code=400)

    if permission == "read":
        if check_ldap_entry(consumer_id, entity, "write", "true"):
            ldap_add_share_entry(consumer_id, entity, read="false", write="true")
        else:
            delete_ldap_entry(consumer_id, entity, "share")
        unbind(consumer_id, entity + ".protected", "#", consumer_id, apikey)
    elif permission == "write":
        if check_ldap_entry(consumer_id, entity, "read", "true"):
            ldap_add_share_entry(consumer_id, entity, read="true", write="false")
        else:
            delete_ldap_entry(consumer_id, entity, "share")
        if "." not in entity:
            delete_ldap_entry(entity+".protected", consumer_id, "exchange")
        else:
            delete_ldap_entry(entity, consumer_id, "exchange")
    elif permission == "read-write":
        delete_ldap_entry(consumer_id, entity, "share")
        unbind(consumer_id, entity + ".protected", "#", consumer_id, apikey)
        if "." not in entity:
            delete_ldap_entry(entity+".protected", consumer_id, "exchange")
        else:
            delete_ldap_entry(entity, consumer_id, "exchange")
    return request.Response(text="unfollow success\n")


def check_ldap_entry(desc, uid, attribute, check_parameter):
    cmd1 = """ldapsearch -H ldap://ldapd:8389 -D "cn=admin,dc=smartcity" -w xRVF!Qowj-3iKWnT -b"""
    cmd2 = """ "description={0},description=share,description=broker,uid={1},cn=devices,dc=smartcity" {2}""".\
        format(desc, uid, attribute)
    cmd = cmd1 + cmd2
    resp = b""
    try:
        resp = subprocess.check_output(cmd, shell=True)
        print(resp)
    except subprocess.CalledProcessError as e:
        print(e)
    check = attribute + ": " + check_parameter
    print(check)
    return bytes(check, 'utf8') in resp


def delete_ldap_entry(desc, uid, entry):
    cmd1 = """ldapdelete -H ldap://ldapd:8389 -D "cn=admin,dc=smartcity" -w xRVF!Qowj-3iKWnT """
    cmd2 = """ "description={0},description={2},description=broker,uid={1},cn=devices,dc=smartcity" """.\
        format(desc, uid, entry)
    cmd = cmd1 + cmd2
    try:
        resp = subprocess.check_output(cmd, shell=True)
        print(resp)
    except subprocess.CalledProcessError as e:
        print(e)


def unshare(request):
    consumer_id = ""
    apikey = ""
    for name, value in request.headers.items():
        if name == "X-Consumer-Username":
            consumer_id = value
        elif name == "Apikey":
            apikey = value
    print(request.text)
    print("consumer_id  : " + str(consumer_id))
    e = json.loads(request.text)
    if "entityID" in e and "permission" in e:
        entity = e["entityID"]  # TODO: check if entity exists in LDAP
        permission = e["permission"]
    else:
        return request.Response(json={'status': 'failure',
                                      'response': 'Input data not in correct format.'}, code=400)
    # exchange applicable for write permission only.
    if "exchange" in e:
        exchange = e["exchange"]
    else:
        exchange = consumer_id + ".protected"

    print("Permission      : " + str(permission))
    print("unfollow Entity : " + str(entity))
    print("exchange applicable for write permission only.")
    print("exchange        : " + str(exchange))

    if permission == "read" or permission == "write" or permission == "read-write":
        pass
    else:
        return request.Response(json={'status': 'failure',
                                      'response': 'permission field not in correct format.'}, code=400)

    if permission == "read":
        if check_ldap_entry(entity, consumer_id, "write", "true"):
            ldap_add_share_entry(entity, consumer_id, read="false", write="true")
        else:
            delete_ldap_entry(entity, consumer_id, "share")
        unbind(entity, consumer_id + ".protected", "#", consumer_id, apikey)
        text = "Read access given to " + entity + " at " + consumer_id + " exchange removed.\n"
        return request.Response(text=text)
    elif permission == "write":
        if check_ldap_entry(entity, consumer_id, "read", "true"):
            ldap_add_share_entry(entity, consumer_id, read="true", write="false")
        else:
            delete_ldap_entry(entity, consumer_id, "share")
        if "." not in entity :
            delete_ldap_entry(consumer_id+".protected", entity, "exchange")
        else:
            delete_ldap_entry(entity, consumer_id, "exchange")
        text = "Write access given to " + entity + " at " + consumer_id + " exchange removed.\n"
        return request.Response(text=text)
    elif permission == "read-write":
        delete_ldap_entry(entity, consumer_id, "share")
        unbind(entity, consumer_id + ".protected", "#", consumer_id, apikey)
        if "." not in entity:
            delete_ldap_entry(consumer_id+".protected", entity, "exchange")
        else:
            delete_ldap_entry(entity, consumer_id, "exchange")
        text = "Read-write access given to " + entity + " at " + consumer_id + " exchange removed.\n"
        return request.Response(text=text)
    return request.Response(text="unshare success\n")

app = Application()
app.router.add_route('/follow', follow, methods=['POST'])
app.router.add_route('/follow', unfollow, methods=['DELETE'])
app.router.add_route('/share', share, methods=['POST'])
app.router.add_route('/share', unshare, methods=['DELETE'])
app.router.add_route('/register', deregister, methods=['DELETE'])
app.run(debug=True)

import json,subprocess,select,hashlib,time,hmac,psycopg2,threading
import queue,configparser

class BatchInsert(object):

    global q,conn,cur,db_lock

    def __init__(self, interval=1):

        self.interval = interval
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):

        while True:

            db_lock.acquire()

            while not q.empty():
                row_list = q.get()
                try:
                    cur.executemany("insert into logs(logline,hash) values(%s,%s)", row_list)
                except psycopg2.DatabaseError as e:
                    print(e)

            db_lock.release()
            conn.commit()

            time.sleep(self.interval)

class WriteToFile(object):

    global file,file_lock

    def __init__(self, interval=1):

        self.interval = interval
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):

        while True:

            file_lock.acquire()

            while not log_queue.empty():
                file = open("/data/logs/kong/kong.log", "a")
                log=log_queue.get()
                file.write(log+"\n")
                file.close()

            file_lock.release()

            time.sleep(self.interval)

def main():
    f = subprocess.Popen(['tail','-F',"-n+1","/data/logs/kong/file.json"], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p = select.poll()
    p.register(f.stdout)

    global sum,count

    while True:
        if p.poll(1):
            s=str(f.stdout.readline())
            s=s[2:-3]
            t = time.time()
            parse(s)
            t1=time.time()-t
            sum+=t1
            print(sum/count)


def parse(log_line):

    global log_queue,file_lock

    formatted=""
    data=dict()

    try:
        data=json.loads(log_line)
    except:
        pass

    if len(data)!=0:

        ip = str(data['client_ip'])

        start_time = data['started_at'] / 1000.0
        timestamp = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(start_time))
        formatted += timestamp + " " + ip + " "

        request_method = str(data['request']['method'])

        temp = str(data['request']['uri']).split("\\/")

        uri=[""]

        try:
            uri = temp[3].split("?")
        except:
            pass


        if (str(uri[0]) == "subscribe" and len(temp) > 3 and len(uri) == 1):
            uri[0] += "Bind"

        formatted += request_method + " " + uri[0] + " "
        resourceId = ""

        try:
            resourceId = str(data['request']['headers']['resourceid'])
        except Exception as e:
            pass

        username = ""
        consumerId = ""

        apikey=""

        try:
            apikey = str(data['request']['headers']['apikey'])
        except:
            pass

        try:
            username = str(data['request']['headers']['x-consumer-username'])
            consumerId = str(data['request']['headers']['x-consumer-id'])
        except Exception as e:
            pass

        response=""
        try:
            response = str(data['response']['status'])
        except:
            pass

        formatted += resourceId + " " + apikey + " " + username + " " + consumerId + " " + response
        formatted=" ".join(formatted.split())

        file_lock.acquire()
        log_queue.put(formatted)
        file_lock.release()

        addHash(formatted)

def addHash(parsed_line):

    global i,rows,last_hash,tup,q,count,hmac_key,first,file,db_lock

    temp_row=()
    temp_row+=(parsed_line,)
    temp = parsed_line.split()

    logLine=""

    prev_hash = ""
    key=""

    if i==0 and first==True:
        hash_object = hmac.new(hmac_key,"smartcity".encode("UTF-8"),digestmod=hashlib.sha512)
        hex_dig = hash_object.hexdigest()
        temp.insert(3,hex_dig)
        first=False
    else:
        temp.insert(3, last_hash)

    logLine = " ".join(temp)


    hash_object=hmac.new(hmac_key,logLine.encode("UTF-8"),digestmod=hashlib.sha512)
    hex_dig = hash_object.hexdigest()
    temp_row+=(hex_dig,)
    temp.insert(len(temp),hex_dig)
    last_hash=hex_dig
    logLine=" ".join(temp)

    print(logLine)
    tup+=(temp_row,)

    i+=1
    count+=1

    if i==100:
        i=0
        db_lock.acquire()
        q.put(tup)
        db_lock.release()
        rows[:]=[]
        tup=()

i = 0
rows=[]
q=queue.Queue()
tup=()
last_hash=""
sum=0
count=1

config = configparser.ConfigParser()
config.read_file(open("/home/pct960/PycharmProjects/LogParser/key.conf"))
db_name=config.get('DATABASE','NAME')
db_user=config.get('DATABASE','USER')
db_password=config.get('DATABASE','PASSWORD')
db_host=config.get('DATABASE','HOST')
db_port=config.get('DATABASE','PORT')
hmac_key=bytearray()
hmac_key.extend(map(ord,str(config.get('HMAC','KEY'))))
conn = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host,port=db_port)
cur = conn.cursor()
db_lock=threading.Lock()
file_lock=threading.Lock()


first=True
log_queue=queue.Queue()
thr=BatchInsert()
thr_write=WriteToFile()

if __name__ == '__main__':
    main()



import json,subprocess,select,time,psycopg2,threading,sys
import queue,configparser

class BatchInsert(object):

    global q,conn,cur,db_lock,tup

    def __init__(self, interval=1):

        self.interval = interval
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):

        global tup
        while True:

            while not q.empty():
                row_list = q.get()
                try:
                    cur.executemany("insert into logs(logline) values(%s)", row_list)
                except psycopg2.DatabaseError as e:
                    print(e)

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

            while not log_queue.empty():
                log=log_queue.get()
                file.write(log+"\n")

            file.flush()
            #os.fsync(file.fileno())
            time.sleep(self.interval)

def main():
    f = subprocess.Popen(['tail','-F',"-n+1","/var/ideam/data/logs/kong/file.json"], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
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
            print(t1)
        else:
            time.sleep(1)

def parse(log_line):

    global log_queue,file_lock,i,tup,count

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
            username = str(data['request']['headers']['x-consumer-username'])
        except Exception as e:
            pass

        response=""
        try:
            response = str(data['response']['status'])
        except:
            pass

        formatted += resourceId + " " + apikey + " " + username + " " + consumerId + " " + response
        formatted=" ".join(formatted.split())

        i+=1

        log_queue.put(formatted)

        temp_row=()
        temp_row+=(formatted,)
        tup+=(temp_row,)
        print(formatted)
        count+=1

        if i == 1000:
            i = 0
            q.put(tup)
            tup=()


i = 0
q=queue.Queue()
tup=()
last_hash=""
sum=0
count=1

ideam_home=str(sys.argv[1])
config = configparser.ConfigParser()
config.read_file(open(ideam_home+"/config/idps/key.conf"))
db_name=config.get('DATABASE','NAME')
db_user=config.get('DATABASE','USER')
db_password=config.get('DATABASE','PASSWORD')
db_host=config.get('DATABASE','HOST')
db_port=config.get('DATABASE','PORT')

file = open("/var/ideam/data/logs/kong/kong.log", "a")
conn = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host,port=db_port)
cur = conn.cursor()

log_queue=queue.Queue()
thr=BatchInsert()
thr_write=WriteToFile()

if __name__ == '__main__':
    main()



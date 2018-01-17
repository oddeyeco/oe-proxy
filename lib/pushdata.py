import requests
import pika
from lib.getconfig import getparam
import lib.daemonlog
import urllib3
import threading
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

uuid = getparam('app', 'uuid')
oddeye_url= getparam('app', 'url')
rabbithost = getparam('app', 'rabbit_host')
rabbituser = getparam('app', 'rabbit_user')
rabbitpass = getparam('app', 'rabbit_pass')

barlus_style = 'UUID=' + uuid + '&data='

credentials = pika.PlainCredentials(rabbituser, rabbitpass)
connection = pika.BlockingConnection(pika.ConnectionParameters(rabbithost, 5672, '/', credentials))
channel = connection.channel()
s = requests.Session()

class Worker(threading.Thread):
    def callback(self, ch, method, properties, body):
        try:
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            s.post(oddeye_url, data=body, verify=False, headers=headers)
        except Exception as err:
            lib.daemonlog.print_message(str(err))
            print(err)

    def __init__(self):
        threading.Thread.__init__(self)
        self.credentials = pika.PlainCredentials(rabbituser, rabbitpass)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(rabbithost, 5672, '/', credentials))
        self.channel = self.connection.channel()
        self.channel.basic_consume(self.callback, queue='OddEye', no_ack=True)
        self.channel.basic_qos(prefetch_count=1)

    def run(self):
        self.channel.start_consuming()

def runworker(wc):
    try:
        for a in range(wc):
            td = Worker()
            td.start()
    except Exception as err:
        lib.daemonlog.print_message(str(err))

import lib.getconfig
import pika

uuid = lib.getconfig.getparam('app', 'uuid')
rabbithost = lib.getconfig.getparam('app', 'rabbit_host')
rabbituser = lib.getconfig.getparam('app', 'rabbit_user')
rabbitpass = lib.getconfig.getparam('app', 'rabbit_pass')

barlus_style = 'UUID=' + uuid + '&data='

class ParseInput(object):
    def __init__(self):
        self.local_vars = {}
        self.data = []
        self.credentials = pika.PlainCredentials(rabbituser, rabbitpass)
        self.params = pika.ConnectionParameters(rabbithost, 5672, '/', self.credentials)
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='OddEye')

    def connect(self):
        if not self.connection or self.connection.is_closed:
            self.connection = pika.BlockingConnection(self.params)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue='OddEye')

    def publish(self, rw):
        self.channel.basic_publish(exchange='', routing_key='OddEye', body=(rw))

    def oddeye(self, rw):
        try:
            self.publish(rw)
            return '200'
        except Exception as err:
            print(err)
            self.connect()
            self.publish(rw)
            return '500'


import lib.getconfig
import pika

datatype = lib.getconfig.getparam('app', 'datatype')
uuid = lib.getconfig.getparam('app', 'uuid')
rabbithost = lib.getconfig.getparam('app', 'rabbit_host')
rabbituser = lib.getconfig.getparam('app', 'rabbit_user')
rabbitpass = lib.getconfig.getparam('app', 'rabbit_pass')

barlus_style = 'UUID=' + uuid + '&data='

credentials = pika.PlainCredentials(rabbituser, rabbitpass)
connection = pika.BlockingConnection(pika.ConnectionParameters(rabbithost, 5672, '/', credentials))
channel = connection.channel()
channel.queue_declare(queue='OddEye')


class ParseInput(object):
    def __init__(self):
        self.local_vars = {}
        self.data = []
    def oddeye(self, rw):
        try:
            channel.basic_publish(exchange='', routing_key='OddEye', body=(rw))
            return 200
        except Exception as err:
            print(err)
            return 500

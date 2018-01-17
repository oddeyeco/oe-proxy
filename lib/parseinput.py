# import json
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

# def influx(self, rw):
#     try:
#         for o in rw.splitlines():
#             do = o.decode()
#             x = do.split(' ')
#             a = x[0].split(',')
#             c = x[1].split('=')
#             self.local_vars['metric'] = a[0]
#             self.local_vars['tags'] = {}
#             self.local_vars['reaction'] = 0
#             self.local_vars['type'] = 'None'
#             self.local_vars['timestamp'] = int(round(int(x[2]) / 1000000000))
#             self.local_vars[c[0]] = float(c[1].replace('i', ''))
#
#             for t in range(1, len(a)):
#                 b = do.split(' ')[0].split(',')[t].split('=')
#                 self.local_vars['tags'][b[0]] = b[1]
#             self.data.append(self.local_vars)
#             self.local_vars = {}
#         json_data = barlus_style + json.dumps(self.data)
#         channel.basic_publish(exchange='',routing_key='OddEye', body=(json_data))
#         return 204
#     except Exception as err:
#         print(err)
#         return 500

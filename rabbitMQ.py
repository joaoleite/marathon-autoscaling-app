from pyrabbit.api import Client

class rabbitMQ:

    _connection = None
    host = None
    web_port = None
    user = None
    password = None

    def __init__(self, host, web_port=15672, user='guest', password='guest'):
        self.host = host
        self.web_port = web_port
        self.user = user
        self.password = password

    def countMessagesQueue(self, vhost, queue):
        cl = Client('{}:{}'.format(self.host, self.web_port), self.user, self.password)
        return cl.get_queue_depth(vhost, queue)


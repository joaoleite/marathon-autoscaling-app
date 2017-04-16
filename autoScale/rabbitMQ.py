from pyrabbit.api import Client
from pyrabbit.http import HTTPError

from autoScale.settings import logger


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
        qtd = 0
        cl = Client('{}:{}'.format(self.host, self.web_port), self.user, self.password)
        try:
            qtd = cl.get_queue_depth(vhost, queue)
        except HTTPError as e:
            logger.error(e)
            raise e
        return  qtd


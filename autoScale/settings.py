import os

import logging


TRUE_LIST = ('true', 'True', 'TRUE', '1', True)


MARATHON_INTERVAL_REFRESH_APP=os.getenv("MARATHON_INTERVAL_REFRESH_APP",60)


LABEL_FOR_AUTOSCALE_ENABLE = 'AUTOSCALE_ENABLE'
LABEL_FOR_AUTOSCALE_RMQ_QUEUE = 'AUTOSCALE_RMQ_QUEUE'
LABEL_FOR_AUTOSCALE_RMQ_VHOST = 'AUTOSCALE_RMQ_VHOST'
LABEL_FOR_AUTOSCALE_RMQ_MAX_MESSAGES_QUEUE = 'AUTOSCALE_RMQ_MAX_MESSAGES_QUEUE'
LABEL_FOR_AUTOSCALE_RMQ_MAX_INSTANCES = 'AUTOSCALE_RMQ_MAX_INSTANCES'
LABEL_FOR_AUTOSCALE_RMQ_MIN_INSTANCES = 'AUTOSCALE_RMQ_MIN_INSTANCES'
LABEL_FOR_AUTOSCALE_RMQ_INCREMENT_INSTANCES = 'AUTOSCALE_RMQ_INCREMENT_INSTANCES'
LABEL_FOR_AUTOSCALE_RMQ_DECREMENT_INSTANCES = 'AUTOSCALE_RMQ_DECREMENT_INSTANCES'

MANDATORY_LABELS_APP = [LABEL_FOR_AUTOSCALE_ENABLE,
                        LABEL_FOR_AUTOSCALE_RMQ_QUEUE,
                        LABEL_FOR_AUTOSCALE_RMQ_MAX_MESSAGES_QUEUE,
                        LABEL_FOR_AUTOSCALE_RMQ_MAX_INSTANCES]

OPTIONAL_LABELS_APP = [LABEL_FOR_AUTOSCALE_RMQ_VHOST,
                       LABEL_FOR_AUTOSCALE_RMQ_MIN_INSTANCES,
                       LABEL_FOR_AUTOSCALE_RMQ_INCREMENT_INSTANCES,
                       LABEL_FOR_AUTOSCALE_RMQ_DECREMENT_INSTANCES]


VAR_MARATHON_HOST = os.getenv('VAR_MARATHON_HOST', '192.168.99.100')
VAR_MARATHON_PORT = int(os.getenv('VAR_MARATHON_PORT', '8080'))
VAR_MARATHON_USE_HTTPS = os.getenv('VAR_MARATHON_USE_HTTPS', False) in TRUE_LIST
VAR_MARATHON_USER = os.getenv('VAR_MARATHON_USER', 'user')
VAR_MARATHON_PASSWORD = os.getenv('VAR_MARATHON_PASSWORD', 'password')

VAR_RABBITMQ_HOST = os.getenv('VAR_RABBITMQ_HOST', '192.168.99.100')
VAR_RABBITMQ_USER = os.getenv('VAR_RABBITMQ_USER', 'user')
VAR_RABBITMQ_PASSWORD = os.getenv('VAR_RABBITMQ_PASSWORD', 'password')
VAR_RABBITMQ_WEB_PORT = os.getenv('VAR_RABBITMQ_WEB_PORT', '15672')



DEBUG = True

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG if DEBUG else logging.WARNING)
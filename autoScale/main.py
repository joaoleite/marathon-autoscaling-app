from time import sleep

from autoScale.marathonAPI import MarathonAPI
from autoScale.rabbitMQ import rabbitMQ
from autoScale.settings import logger, VAR_MARATHON_HOST
from autoScale.settings import VAR_MARATHON_PORT, VAR_MARATHON_USE_HTTPS, VAR_MARATHON_PASSWORD, VAR_MARATHON_USER, \
                                VAR_RABBITMQ_WEB_PORT, VAR_RABBITMQ_PASSWORD, VAR_RABBITMQ_USER, VAR_RABBITMQ_HOST

logger.info('Configurating MarathonAPI...')
host = MarathonAPI(host=VAR_MARATHON_HOST, port=VAR_MARATHON_PORT, use_https=VAR_MARATHON_USE_HTTPS, user=VAR_MARATHON_USER, password=VAR_MARATHON_PASSWORD)

logger.info('Configurating RabbitMQ...')
target  = rabbitMQ(host=VAR_RABBITMQ_HOST, user=VAR_RABBITMQ_USER, password=VAR_RABBITMQ_PASSWORD, web_port=VAR_RABBITMQ_WEB_PORT)

stop = False
while (not stop):
    host.findAppsWithAutoscaleLabels()
    host.scaleApps(target)
    sleep(15)


fim = True





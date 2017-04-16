from time import sleep

from autoScale.marathonAPI import MarathonAPI
from autoScale.rabbitMQ import rabbitMQ
from autoScale.settings import logger

logger.info('Configurating MarathonAPI...')
host = MarathonAPI(host='192.168.99.100', port=8080)

logger.info('Configurating RabbitMQ...')
target  = rabbitMQ(host='192.168.99.100', user='user', password='password')

stop = False
while (not stop):
    host.findAppsWithAutoscaleLabels()
    host.scaleApps(target)
    sleep(15)


fim = True





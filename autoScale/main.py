from marathonAPI import MarathonAPI
from rabbitMQ import rabbitMQ
from settings import VAR_MARATHON_PORT, VAR_MARATHON_USE_HTTPS, VAR_MARATHON_PASSWORD, VAR_MARATHON_USER, \
    VAR_RABBITMQ_WEB_PORT, VAR_RABBITMQ_PASSWORD, VAR_RABBITMQ_USER, VAR_RABBITMQ_HOST
from settings import MARATHON_INTERVAL_REFRESH_APP
from settings import logger, VAR_MARATHON_HOST

logger.info('Configurating MarathonAPI...')
host = MarathonAPI(host=VAR_MARATHON_HOST, port=VAR_MARATHON_PORT, use_https=VAR_MARATHON_USE_HTTPS, user=VAR_MARATHON_USER, password=VAR_MARATHON_PASSWORD)

logger.info('Configurating RabbitMQ...')
target  = rabbitMQ(host=VAR_RABBITMQ_HOST, user=VAR_RABBITMQ_USER, password=VAR_RABBITMQ_PASSWORD, web_port=VAR_RABBITMQ_WEB_PORT)

import asyncio
def callback(n, loop):
    try:
        host.findAppsWithAutoscaleLabels()
        host.scaleApps(target)
    except Exception as e:
        logger.error(e)
    finally:
        now = loop.time()
        loop.call_at(now + n, callback, n, loop)


async def main(loop):
    delta_time = MARATHON_INTERVAL_REFRESH_APP
    loop.call_soon(callback, delta_time, loop)
    while True:
        await asyncio.sleep(1)

event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()

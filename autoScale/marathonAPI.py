from marathon import MarathonHttpError, MarathonClient
from autoScale.settings import logger, LABEL_FOR_AUTOSCALE_ENABLE, MANDATORY_LABELS_APP, OPTIONAL_LABELS_APP


class MarathonApp(object):
    id = None
    tasksRunning = None
    tasksStaged = None

    AUTOSCALE_ENABLE = 0
    AUTOSCALE_RMQ_QUEUE = None
    AUTOSCALE_RMQ_VHOST = '/'
    AUTOSCALE_RMQ_MAX_MESSAGES_QUEUE = None
    AUTOSCALE_RMQ_MAX_INSTANCES = None
    AUTOSCALE_RMQ_MIN_INSTANCES = 1
    AUTOSCALE_RMQ_INCREMENT_INSTANCES = 1
    AUTOSCALE_RMQ_DECREMENT_INSTANCES = 1

    def __init__(self, id) -> None:
        self.id = id

    def scaneRequired(self, rabbitmq):
        delta = 0
        required = True
        currentQtd= rabbitmq.countMessagesQueue(self.AUTOSCALE_RMQ_VHOST, self.AUTOSCALE_RMQ_QUEUE)

        # Se existe mais mensagem do que o definido
        if currentQtd >= self.AUTOSCALE_RMQ_MAX_MESSAGES_QUEUE:
            qtd_faltam = (self.AUTOSCALE_RMQ_MAX_INSTANCES - self.tasksRunning)
            # Precisa aumentar a qtd de workers
            if qtd_faltam > 0:
                delta = self.AUTOSCALE_RMQ_INCREMENT_INSTANCES
                required = True
            # Está no maximo dos workers
            elif qtd_faltam == 0:
                delta = 0
                required = False
            # Passou (??) da quantidade maxima de worker
            else:
                pass
        # Se a fila zerou, volta para o minimo
        elif currentQtd == 0:
            delta = (self.AUTOSCALE_RMQ_MIN_INSTANCES - self.tasksRunning)
            if delta == 0:
                required = False
            else:
                required = True
        # Se a fila está menor do que o max tem que diminuir
        elif currentQtd < self.AUTOSCALE_RMQ_MAX_MESSAGES_QUEUE:
            delta = self.AUTOSCALE_RMQ_DECREMENT_INSTANCES
            required = True

        return [required, delta]





class MarathonAPI(object):
    user = None
    password = None
    host = None
    use_https = False
    port = None
    url = None
    marathon_cli = None
    dict_apps = {}

    def __init__(self, host, port=80, use_https=False, user=None, password=None ):
        self.user = user
        self.password = password
        self.host = host
        self.use_https = use_https
        self.port = str(port)
        self.url = '{}://{}:{}/'.format('https' if use_https else 'http', host, port)
        try:
            self.marathon_cli = MarathonClient([self.url],username=self.user, password=self.password)
        except Exception as e:
            logger.critical(e)
            raise e

    def scaleOneApp(self, app_id, delta=None):
        logger.info('App: [{}] :: Scale {} Delta:[{}] Atual:[{}] Staged:[{}]'.format(app_id,
                                                                                     'up' if delta > 0 else 'down',
                                                                                     delta,
                                                                                     self.dict_apps[app_id].tasksRunning,
                                                                                     self.dict_apps[app_id].tasksStaged))
        try:
            self.marathon_cli.scale_app(app_id=app_id, delta=delta)
        except MarathonHttpError as e:
            logger.error(e.error_message)
        except:
            raise


    def findAppsWithAutoscaleLabels(self):
        list = self.marathon_cli.list_apps(embed_counts=True, embed_task_stats=True)
        logger.critical('Lista recebida {}'.format(list))
        if len(list) == 0:
            logger.warning('0 apps loaded. Your marathon have apps?')
        for app in list:
            if LABEL_FOR_AUTOSCALE_ENABLE in app.labels:
                new_app = MarathonApp(app.id)
                new_app.tasksRunning = app.tasks_running
                new_app.tasksStaged = app.tasks_staged
                for label in MANDATORY_LABELS_APP:
                    if label in app.labels:
                        value = app.labels[label]
                        if value.isnumeric():
                            value = int(value)
                        new_app.__setattr__(label, value)
                    else:
                        logger.error('App: [{}] :: dont have MANDATORY_LABELS :: {}'.format(app.id, label))
                for label in OPTIONAL_LABELS_APP:
                    if label in app.labels:
                        value = app.labels[label]
                        if value.isnumeric():
                            value = int(value)
                        new_app.__setattr__(label, value)
                self.dict_apps[app.id] = new_app
            else:
                logger.debug('App: [{}] :: dont have {} = True. If you want to scale, please add labels.'.format(app.id, LABEL_FOR_AUTOSCALE_ENABLE))

    def scaleApps(self, rabbitmq):
        for app_id in self.dict_apps:
            app = self.dict_apps[app_id]
            required, delta = app.scaneRequired(rabbitmq)
            if required:
                self.scaleOneApp(app_id=app_id, delta=delta)
            else:
                logger.info('App: [{}] :: Not Required Scale'.format(app_id))

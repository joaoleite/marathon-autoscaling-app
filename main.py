from time import sleep
from marathonAPI import MarathonAPI
from rabbitMQ import rabbitMQ

host = MarathonAPI(host='192.168.99.100', port=8080)
target  = rabbitMQ(host='192.168.99.100', user='user', password='password')

stop = False
while (not stop):
    host.findAppsWithAutoscaleLabels()
    host.scaleApps(target)
    sleep(15)


fim = True





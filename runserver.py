'''
Created on 13/set/2014

@author: Vincenzo Pirrone <pirrone.v@gmail.com>
'''

from osnf.ws import app
from osnf.sensors import Sensor
from conf.settings import HOST, PORT
from cherrypy import wsgiserver

d = wsgiserver.WSGIPathInfoDispatcher({'/': app})
server = wsgiserver.CherryPyWSGIServer((HOST, PORT), d)

if __name__ == '__main__':
    try:
        sensor = Sensor()
        server.start()
    except KeyboardInterrupt:
        server.stop()
        sensor.exit()

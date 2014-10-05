'''
Created on 13/set/2014

@author: Vincenzo Pirrone <pirrone.v@gmail.com>
'''

import osnf.ws as ws
from osnf.core import build_network
from conf.node import LISTEN_ADDR, PORT
from cherrypy import wsgiserver


 
d = wsgiserver.WSGIPathInfoDispatcher({'/': ws.app})
server = wsgiserver.CherryPyWSGIServer((LISTEN_ADDR, PORT), d)


if __name__ == '__main__':
    network = build_network()
    try:
        network.start()
        server.start()
    except KeyboardInterrupt:
        server.stop()
        network.stop()

'''
Created on 13/set/2014

@author: Vincenzo Pirrone <pirrone.v@gmail.com>
'''

import osnf.ws as ws
from osnf.core import Node
from conf.settings import HOST, PORT
from cherrypy import wsgiserver


 
d = wsgiserver.WSGIPathInfoDispatcher({'/': ws.app})
server = wsgiserver.CherryPyWSGIServer((HOST, PORT), d)


if __name__ == '__main__':
    node = Node()
    try:
        node.start()
        server.start()
    except KeyboardInterrupt:
        server.stop()
        node.exit()

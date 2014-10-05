'''
Created on 13/set/2014

@author: Vincenzo Pirrone <pirrone.v@gmail.com>
'''


from conf.node import stations, NAME, DESCRIPTION
from osnf.api import Node, Network


network = None


   

class LocalNode(Node):
    

    def _init_station(self, key, desc):
        if not desc.has_key('enabled') or desc['enabled']:
            Class = desc['class']
            data = desc['data'] if desc.has_key('data') else {}
            monitors = desc['monitors'] if desc.has_key('monitors') else []
            st = Class(name=key, description=desc['description'], connector=desc['connector'], data=data, monitors=monitors)
            self.stations[key] = st
    
    
    def __init__(self, name, description):
        Node.__init__(self, name, description)
        self.stations = {}
        for key in stations.keys():
            self._init_station(key, stations[key])
            
    def get_station(self, name):
        return self.stations[name]
    
    def start(self):
        for st in self.stations.values():
            st.start()
    
    def stop(self):
        for st in self.stations.values():
            st.stop()
    
class NetworkImpl(Network):
    
    def __init__(self):
        self.local_node = LocalNode(NAME, DESCRIPTION)
        
    def get_node(self, name):
        return self.local_node
    
    def start(self):
        self.local_node.start()
    
    def stop(self):
        self.local_node.stop()
    
def get_network():
    return network
        
def build_network():
    global network 
    network = NetworkImpl()
    return network



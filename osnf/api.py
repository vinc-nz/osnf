'''
Created on 28/set/2014

@author: Vincenzo Pirrone <pirrone.v@gmail.com>
'''

network = None

def get_network():
    return network

def set_network_object(net_obj):
    network = net_obj

class Network:
    
    def get_node(self, name):
        pass
    
    def start(self):
        pass    
    
    def stop(self):
        pass
    

class Node:
    
    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    def get_station(self, name):
        pass
    

class Station:
    
    def __init__(self, name, description, connector, data={}, monitors=[]):
        self.name = name
        self.description = description
        self.connector = connector
        self.data = data
        self.monitors = {}
        for m in monitors:
            self.register_monitor(m)
      
    def register_monitor(self, m):
        if m.enabled:
                if self.monitors.has_key(m.key):
                    self.monitors[m.key].append(m)
                else:
                    self.monitors[m.key] = [m]  
        
    def start(self):
        pass    
    
    def stop(self):
        self.connector.close()
    

    

class ValueMonitor:
    
    def __init__(self, key, enabled=True):
        self.key = key
        self.enabled = enabled
        
    def on_value_change(self, network, oldvalue, newvalue):
        pass

    

'''
Created on 13/set/2014

@author: Vincenzo Pirrone <pirrone.v@gmail.com>
'''

import threading, time

from conf.node import stations, nodes, rules


def get_local_node():
    for node in nodes:
        if nodes[node]['address'] == '127.0.0.1':
            return node
        


class Node(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.init_stations()
        self.active = True
        self.lock = threading.Lock()
        
    def init_stations(self):
        for st in stations:
            desc = stations[st]
            port = desc['port']
            desc['instance'] = desc['class'](port)
            
    def close_stations(self):
        for st in stations:
            desc = stations[st]
            desc['instance'].exit()
    
    def is_active(self):
        self.lock.acquire()
        val = self.active
        self.lock.release()
        return val
            
    def run(self):
        while self.is_active():
            for rule in rules:
                self._run_rule(rules[rule])
            time.sleep(1)
        
    def _run_rule(self, rule):
        if int(time.time()) % rule['run_interval'] == 0:
            rule_func = rule['function']
            rule_func()
            
    def exit(self):
        self.lock.acquire()
        self.active = False
        self.lock.release()
        self.close_stations()
        
    
        

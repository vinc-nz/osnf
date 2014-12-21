'''
Created on 05/ott/2014

@author: Vincenzo Pirrone <pirrone.v@gmail.com>
'''
import re
import threading

from osnf.api import Station
from osnf.api import get_network


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()
        
    def is_running(self):
        return not self._stop.isSet()


class Sensor(StoppableThread, Station):
    
    def __init__(self, name, description, connector, data={}, monitors=[]):
        StoppableThread.__init__(self)
        Station.__init__(self, name, description, connector, data=data, monitors=monitors)
        self.pattern = re.compile('\w+:\d+')
        self.mapping = {'TEMP' : 'temperature', 'HUM' : 'humidity', 'LIGHT' : 'brightness', 'TIME' : 'time' }
        self.types = {'TEMP' : float, 'HUM' : float, 'LIGHT' : float, 'TIME' : int }
    
    def run(self):
        StoppableThread.run(self)
        while self.is_running():
            values = self._read()
            for st_key in values.keys():
                converter = self.types[st_key]
                osnf_key = self.mapping[st_key]
                st_val = converter(values[st_key])
                self._update(osnf_key, st_val)
                    
    def _update(self, key, val):
        oldval = None
        if self.data.has_key(key):
            oldval = self.data[key]
        if oldval is None or oldval != val:
            self.data[key] = val
            if self.monitors.has_key(key):
                monitors = self.monitors[key]
                for m in monitors:
                    m.on_value_change(get_network(), oldval, val)
    
    
    def _read(self):
        #print 'DEBUG: reading from serial'
        values = {}
        line = self.connector.readline()
        while not self.pattern.search(line):
            line = self.connector.readline()
        l = line.rstrip('\n').split(',')
        for elem in l:
            try:
                (key, value) = elem.split(':')
                values[key] = value
            except Exception:
                print 'ERROR: _read error reading ' + str(elem)
        #print 'DEBUG: read all:' + values
        return values
    
    
    def get_all_data(self):
        return dict(self.data)
        
    def get_data(self, key):
        if self.data.has_key(key):
            return self.data[key]
        return None
    


class Switch(Station):
    
    def __init__(self, name, description, connector, data={}, monitors=[]):
        Station.__init__(self, name, description, connector, data=data, monitors=monitors)
        self.on = False
    
    def turn_on(self):
        if not self.on:
            self.connector.writeline('a')
            self.on = True
        
    def turn_off(self):
        if self.on:
            self.connector.writeline('s')
            self.on = False
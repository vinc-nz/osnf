'''
Created on 13/set/2014

@author: Vincenzo Pirrone <pirrone.v@gmail.com>
'''

import re
import threading


class FakeSerial():
    def __init__(self, port):
        print 'opening fake serial on %s' % port
    
    def readline(self):
        return 'TEMP:26,HUM:70,LIGHT:50\n'
    
    def write(self, line):
        print 'FAKE SERIAL: ' + line
    
    def close(self):
        print 'closing fake serial'
    
class Station:
    def __init__(self, port):
        print 'DEBUG: opening serial ' + port
        try:
            from conf.settings import SERIAL_CLASS
        except ImportError:
            print 'DEBUG: using fake serial'
            SERIAL_CLASS=FakeSerial
        self.serial = SERIAL_CLASS(port)   
        
    def exit(self):
        self.serial.close() 
       
class Sensor(Station, threading.Thread):
    def __init__(self, port):
        Station.__init__(self, port)
        threading.Thread.__init__(self)
        print 'instancing Sensor'
        self.pattern = re.compile('\w+:\d+')
        self.values = {}
        self.lock = threading.Lock()
        self.active = True
        self.start()
        
    def is_active(self):
        self.lock.acquire()
        val = self.active
        self.lock.release()
        return val
        
    def run(self):
        threading.Thread.run(self)
        while self.is_active():
            values = self._read()
            for k in values.keys():
                self.values[k] = values[k]
        
    def _read(self):
        #print 'DEBUG: reading from serial'
        values = {}
        line = self.serial.readline()
        while not self.pattern.search(line):
            line = self.serial.readline()
        l = line.rstrip('\n').split(',')
        for elem in l:
            try:
                (key, value) = elem.split(':')
                values[key] = value
            except Exception:
                print 'ERROR: _read error reading ' + str(elem)
        #print 'DEBUG: read all:' + values
        return values
    
    def get_values(self):
        values = self.values
        temp = float(values['TEMP']) if values.has_key('TEMP') else 0
        hum = float(values['HUM']) if values.has_key('HUM') else 0
        light = float(values['LIGHT']) if values.has_key('LIGHT') else 0
        return {
                'temperature' : temp,
                'humidity' : hum,
                'brightness' : light,
                'position' : {'latitude' : 39.343495, 'longitude' : 16.194757}
         }
        
    def get_value(self, key):
        return self.get_values()[key]
    
    def exit(self):
        Station.exit(self)
        self.lock.acquire()
        self.active = False
        self.lock.release()
    
   
        
class Switch(Station):
    
    def __init__(self, port):
        Station.__init__(self, port)
        print 'instancing Switch'
        self.on = False
        
    def turn_on(self):
        if not self.on:
            self.serial.write('a\n')
            self.on = True
        
    def turn_off(self):
        if self.on:
            self.serial.write('s\n')
            self.on = False
  
        
if __name__ == '__main__':
    s= Sensor()
    print s.read_value('HUM')
    print s.read_all()


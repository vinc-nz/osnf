'''
Created on 13/set/2014

@author: Vincenzo Pirrone <pirrone.v@gmail.com>
'''

import re

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

class FakeSerial():
    def __init__(self, port, baudrate):
        print 'opening fake serial'
    
    def readline(self):
        return 'TEMP:26,HUM:70,LIGHT:50\n'
    
    def close(self):
        print 'closing fake serial'
       
@singleton
class Sensor:
    def __init__(self):
        print 'DEBUG: opening serial'
        try:
            from conf.settings import SERIAL_CLASS
        except ImportError:
            print 'DEBUG: using fake serial'
            SERIAL_CLASS=FakeSerial
        self.serial = SERIAL_CLASS('/dev/ttyACM0', baudrate=9600)
        self.pattern = re.compile('TEMP:\d+,HUM:\d+,LIGHT:\d+')
        
    def read_all(self):
        print 'DEBUG: read all'
        values = {}
        line = self.serial.readline()
        if not self.pattern.search(line):
            line = 'TEMP:0,HUM:0,LIGHT:0\n'
        l = line.rstrip('\n').split(',')
        for elem in l:
            (key, value) = elem.split(':')
            values[key] = value
        #print 'DEBUG: read all:' + values
        return values
        
    def read_value(self, key):
        line = self.serial.readline()
        print 'DEBUG: serial: %s' % line
        return re.search(key + ':(\d+)', line).group(1)
    
    def exit(self):
        self.serial.close()
        
if __name__ == '__main__':
    s= Sensor()
    print s.read_value('HUM')
    print s.read_all()


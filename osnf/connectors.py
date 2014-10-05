'''
Created on 28/set/2014

@author: Vincenzo Pirrone <pirrone.v@gmail.com>
'''

import serial, time


class Connector:
    
    def readline(self):
        pass
    
    def writeline(self, line):
        pass
    
    def close(self):
        pass


class FakeSerial(Connector):
    def __init__(self, port):
        print 'opening fake serial on %s' % port
    
    def readline(self):
        time.sleep(2)
        return 'TIME:%d' % int(time.time())
    
    def writeline(self, line):
        print 'FAKE SERIAL: ' + line
    
    def close(self):
        print 'closing fake serial'



class Serial(Connector, serial.Serial):
    def __init__(self, 
        port=None, 
        baudrate=9600, 
        bytesize=serial.EIGHTBITS, 
        parity=serial.PARITY_NONE, 
        stopbits=serial.STOPBITS_ONE, 
        timeout=None, 
        xonxoff=False, 
        rtscts=False, 
        writeTimeout=None, 
        dsrdtr=False, 
        interCharTimeout=None):
        
        serial.Serial.__init__(self, port=port, baudrate=baudrate, bytesize=bytesize, parity=parity, stopbits=stopbits, timeout=timeout, xonxoff=xonxoff, rtscts=rtscts, writeTimeout=writeTimeout, dsrdtr=dsrdtr, interCharTimeout=interCharTimeout)
        

    def readline(self):
        return Serial.readline(self)
    
    def writeline(self, line):
        Serial.write(self, line + '\n')
        
    def close(self):
        Serial.close(self)
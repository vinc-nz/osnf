'''
Created on 13/set/2014

@author: Vincenzo Pirrone <pirrone.v@gmail.com>
'''

import serial

HOST='0.0.0.0'
PORT=80
SERIAL_CLASS=serial.Serial

try:
    from conf.local_settings import *
except ImportError:
    pass
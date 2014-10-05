'''
Created on 13/set/2014

@author: Vincenzo Pirrone <pirrone.v@gmail.com>
'''


from osnf.api import ValueMonitor
from osnf.connectors import Serial, FakeSerial
from osnf.stations import Switch, Sensor


NAME = 'nodo1'
DESCRIPTION = ''
LISTEN_ADDR = '0.0.0.0'
PORT = 5000


remote_nodes = {}


class LightMonitor(ValueMonitor):
    
    def __init__(self, enabled=True):
        ValueMonitor.__init__(self, key='brightness', enabled=enabled)
        
    def on_value_change(self, network, oldvalue, newvalue):
        light = newvalue
        switch = network.get_local_node().get_station('OSA2')
        if light < 50:
            switch.turn_on()
        else:
            switch.turn_off()

class Clock(ValueMonitor):
    
    def __init__(self, enabled=True):
        ValueMonitor.__init__(self, key='time', enabled=enabled)
        
    def on_value_change(self, network, oldvalue, newvalue):
        print newvalue

stations = {
               
    'OSA1' : {
        'class' : Sensor,
        'connector' : FakeSerial(port='/dev/ttyACM0'),
        'description' : 'Rileva temperatura, umidita, luminosita',
        'data' : {
            'position' : {'latitude' : 39.343495, 'longitude' : 16.194757}
        },
        'monitors' : [
            LightMonitor(enabled=False),
            Clock()
        ]
    },
            
    'OSA2' : {
        'class' : Switch,
        'connector' : FakeSerial(port='/dev/ttyACM1'),
        'description' : 'Interruttore con LED',
    }
  
}




        
# { "node" : "nodo1", "station" : "OSA1", "timestamp_minute" : current_minute, "type" : "position", "value" : position_content.position };
# { "node" : "nodo1", "station" : "OSA1", "timestamp_minute" : current_minute, "type" : "humidity", "value" : humidity_content.humidity };
# { "node" : "nodo1", "station" : "OSA1", "timestamp_minute" : current_minute, "type" : "temperature", "value" : temperature_content.temperature };
# { "node" : "nodo1", "station" : "OSA1", "timestamp_minute" : current_minute, "type" : "brightness", "value" : brightness_content.brightness };



    

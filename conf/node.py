'''
Created on 13/set/2014

@author: Vincenzo Pirrone <pirrone.v@gmail.com>
'''

import json

import requests

from osnf.stations import Sensor, Switch


local_name = 'nodo1'


remote_nodes = {}

stations = {
               
    'OSA1' : {
        'port' : '/dev/ttyACM0',
        'class' : Sensor,
        'description' : 'Rileva temperatura, umidita, luminosita',
    },
            
    'OSA2' : {
        'port' : '/dev/ttyACM1',
        'class' : Switch,
        'description' : 'Interruttore con LED',
    }
  
               
}


    
def remote_switch():
    light = stations['OSA1']['instance'].get_value('brightness')
    node = remote_nodes['nodo2']
    endpoint = "http://%s:%s/v2/nodo2/OSA2/switch" % (node['address'], node['port'])
    headers = {'content-type': 'application/json'}
    if light < 50:
        requests.post(endpoint, headers=headers, data=json.dumps({'switch': 'on'}))
    else:
        requests.post(endpoint, headers=headers, data=json.dumps({'switch': 'off'}))
        
def local_switch():
    light = stations['OSA1']['instance'].get_value('brightness')
    switch = stations['OSA2']['instance']
    if light < 50:
        switch.turn_on()
    else:
        switch.turn_off()

rules = {
    'RULE1' : {
        'run_interval' : 1,
        'function' : local_switch,
        'name' : 'Regola del LED',
        'description' : 'Accende o spegne il LED in base al valore della luminosita',
        'enabled' : False
    }
}


        
# { "node" : "nodo1", "station" : "OSA1", "timestamp_minute" : current_minute, "type" : "position", "value" : position_content.position };
# { "node" : "nodo1", "station" : "OSA1", "timestamp_minute" : current_minute, "type" : "humidity", "value" : humidity_content.humidity };
# { "node" : "nodo1", "station" : "OSA1", "timestamp_minute" : current_minute, "type" : "temperature", "value" : temperature_content.temperature };
# { "node" : "nodo1", "station" : "OSA1", "timestamp_minute" : current_minute, "type" : "brightness", "value" : brightness_content.brightness };



    

'''
Created on 13/set/2014

@author: Vincenzo Pirrone <pirrone.v@gmail.com>
'''

from osnf.stations import Sensor, Switch


nodes = { 
    'nodo1' : {
        'address' : '127.0.0.1',
        'port' : 80,
        'code' : 'nodo1',
        'name' : 'Test',
        'description' : 'Bla bla'
    }
}

stations = {
               
    'OSA1' : {
        'port' : '/dev/ttyACM0',
        'class' : Sensor,
        'name' : 'Stazione 1',
        'description' : 'Rileva temperatura, umidita, luminosita',
        'show' : True
    },
               
    'OSA2' : {
        'port' : '/dev/ttyACM1',
        'class' : Switch,
        'name' : 'Stazione 2',
        'description' : 'Interruttore con LED',
        'show' : False
    }
}


    
def my_rule():
    light = stations['OSA1']['instance'].get_value('brightness')
    switch = stations['OSA2']['instance']
    if light < 50:
        switch.turn_on()
    else:
        switch.turn_off()

rules = {
    'RULE1' : {
        'run_interval' : 1,
        'function' : my_rule,
        'name' : 'Regola del LED',
        'description' : 'Accende o spegne il LED in base al valore della luminosita'
    }
}


        




    
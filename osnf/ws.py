'''
Created on 13/set/2014

@author: Vincenzo Pirrone <pirrone.v@gmail.com>
'''

from flask import Flask
from osnf.sensors import Sensor
import json
app = Flask(__name__)


def read_all():
    sensor = Sensor()
    values = sensor.read_all()
    return {
         'temperature' : values['TEMP'],
         'humidity' : values['HUM'],
         'brightness' : values['LIGHT'],
         'position' : {'latitude' : 52.5, 'longitude' : 5.75}
         }

@app.route('/')
def hello_world():
    return json.dumps(read_all())


@app.route('/temperature')
def temperature():
    return json.dumps({'temperature' : read_all()['temperature']})

@app.route('/humidity')
def humidity():
    return json.dumps({'humidity' : read_all()['humidity']})

@app.route('/brightness')
def brightness():
    return json.dumps({'brightness' : read_all()['brightness']})

@app.route('/position')
def position():
    return json.dumps({'position' : read_all()['position']})

if __name__ == '__main__':
    app.debug = True
    app.run()
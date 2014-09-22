'''
Created on 13/set/2014

@author: Vincenzo Pirrone <pirrone.v@gmail.com>
'''

import json

from flask import Flask
from flask_cors import CORS

from conf.node import nodes, stations
import core


app = Flask(__name__)
app.debug = True
cors = CORS(app)




@app.route('/v1/temperature')
def temperature():
    return json.dumps({'temperature' : 25})

@app.route('/v1/humidity')
def humidity():
    return json.dumps({'humidity' : 70})

@app.route('/v1/brightness')
def brightness():
    return json.dumps({'brightness' : 80})

@app.route('/v1/position')
def position():
    return json.dumps({'position' : {'latitude' : 39.343495, 'longitude' : 16.194757}})

@app.route('/v2')
def get_nodes():
    return json.dumps(nodes)


@app.route('/v2/<node>')
def get_stations(node):
    return to_json(stations)

@app.route('/v2/<node>/<st>')
def get_values(node, st):
    st_instance = stations[st]['instance']
    return json.dumps(st_instance.get_values())
    
@app.route('/v2/<node>/<st>/<key>')
def get_value(node, st, key):
    st_instance = stations[st]['instance']
    return json.dumps({key : st_instance.get_value(key)})

def to_json(api_elem):
    whitelist = ['name', 'description']
    d = {}
    for code in api_elem:
        desc = api_elem[code]
        d[code] = { k: desc[k] for k in whitelist }
    return json.dumps(d)





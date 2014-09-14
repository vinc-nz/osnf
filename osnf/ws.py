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


def to_json(api_elem):
    whitelist = ['name', 'description']
    d = {}
    for code in api_elem:
        desc = api_elem[code]
        d[code] = { k: desc[k] for k in whitelist }
    return json.dumps(d)


def init_ws():
    root = '/v2/'
    local_node = core.get_local_node()
    print 'local node is %s' % local_node
    def view_func() : return to_json(stations)
    app.add_url_rule(root + local_node, local_node, view_func)
    for st in stations:
        map_station(st, root + local_node + '/' + st)
        
def map_station(st, st_root):
    st_desc = stations[st]
    if st_desc['show']:
        st_instance = st_desc['instance']
        print 'binding %s with %s' % (st_root, str(st_instance))
        def view_func(): return json.dumps(st_instance.get_values())
        app.add_url_rule(st_root, st, view_func)
        map_sensor(st_instance, st_root + '/', 'temperature')
        map_sensor(st_instance, st_root + '/', 'humidity')
        map_sensor(st_instance, st_root + '/', 'brightness')
        map_sensor(st_instance, st_root + '/', 'position')
        
def map_sensor(sensor, root, key):
    endpoint = root + key
    def view_func(): return json.dumps({key : sensor.get_value(key)})
    app.add_url_rule(endpoint, endpoint, view_func)


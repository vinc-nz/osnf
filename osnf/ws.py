'''
Created on 13/set/2014

@author: Vincenzo Pirrone <pirrone.v@gmail.com>
'''

import json

from flask import Flask
from flask.globals import request
from flask_cors import CORS

from conf.node import remote_nodes, NAME, DESCRIPTION, LISTEN_ADDR, stations
from osnf.api import get_network


app = Flask(__name__)
app.debug = True
cors = CORS(app)




@app.route('/api')
def get_nodes():
    nodes = dict(remote_nodes)
    nodes[NAME] = {'description' : DESCRIPTION, 'listen_addr' : LISTEN_ADDR}
    return json.dumps(nodes)

@app.route('/api/<node>')
def get_stations(node):
    response = {}
    for k in stations.keys():
        response[k] = stations[k]['description']
    return json.dumps(response)
        

@app.route('/api/<node>/<st>')
def get_all_data(node, st):
    st_instance = get_network().get_node(node).get_station(st)
    return json.dumps(st_instance.get_all_data())
    
@app.route('/api/<node>/<st>/<key>')
def get_value(node, st, key):
    st_instance = get_network().get_node(node).get_station(st)
    return json.dumps({key : st_instance.get_data(key)})

@app.route('/api/<node>/<st>/<key>', methods=['POST'])
def change_state(node, st, key):
    rpc = request.get_json()
    st_instance = get_network().get_node(node).get_station(st)
    if key == 'switch':
        if rpc['switch'] == 'on':
            st_instance.turn_on()
        elif rpc['switch'] == 'off':
            st_instance.turn_off()
    return ('', 204)








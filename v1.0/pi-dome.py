#!/usr/bin/python
# ====================================================================
# The pi-dome script was a idea I had after seeing a garage door 
# youtube video where a raspberry pi was used with a 5v relay to open
# the garage over wifi.
#
# Copyright (C) 2014 by TekZap Co. 
# All Rights Reserved.
# https://github.com/metzenw/pi-dome

# ====================================================================
# The MIT License (MIT)
#
# Copyright (c) 2014 TekZap Co.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE
# ====================================================================

# ====================================================================
# Import from libraries 
# ====================================================================
import ConfigParser

from flask import Flask, jsonify, abort, make_response, request
from flask.ext.httpauth import HTTPBasicAuth, HTTPDigestAuth

# Read in conf file
config = ConfigParser.ConfigParser()
config.read('dome.cfg')


PI_DOME_VERSION = config.get('MASTER', 'VERSION', 0)   # Pi-dome version.
AUTHOR = "Jason Booth"                                 # The author (me).
AUTHOR_EMAIL = "metzenw at gmail (dot) com"            # My email. Report bugs here or via github.com.
GIT_REPO = "https://github.com/metzenw/pi-dome"        # Repo address.

# Setting up username and password for http auth user.
if config.get('MASTER', 'HTTP_AUTH_USER', 0):
    HTTP_AUTH_USER = config.get('MASTER', 'HTTP_AUTH_USER', 0)
else:
    HTTP_AUTH_USER = "pi-dome"
if config.get('MASTER', 'HTTP_AUTH_PASSWORD', 0):
    HTTP_AUTH_PASSWORD = config.get('MASTER', 'HTTP_AUTH_PASSWORD', 0)
else:
    HTTP_AUTH_PASSWORD = "pi-dome"

# Setup flask
app = Flask(__name__)

# Setup HTTPAuth
auth = HTTPBasicAuth()
@auth.get_password
def get_password(username):
    if username == HTTP_AUTH_USER:
        return HTTP_AUTH_PASSWORD
    return None

# HTTPAuth failed to access responce
@auth.error_handler
def unauthorized():
    return make_response( jsonify( { 'error': 'Unauthorized access' } ), 401 )


# Supported resources that pi-dome manages.
# doors, windows, garage, temps, motion_sensors, pi-nodes, pi-servers
doors = [
    {
        'id': 1,
        'type': u'door',
        'gpio': 11,
        'voltage': 3.3,
        'notes': u'Some notes.',
        'description': u'Garage door up.', 
        'open': False
    },
    {
        'id': 2,
        'type': u'door',
        'gpio': 13,
        'voltage': 3.3,
        'notes': u'Some notes.',
        'description': u'Garage door down.', 
        'open': False
    }
]

windows = [
    {
        'id': 1,
        'type': u'window',
        'gpio': 0,
        'voltage': 3.3,
        'notes': u'Some notes.',
        'description': u'Place Holder.',
        'open': False
    }
]

garage = [
    {
        'id': 1,
        'type': u'garage',
        'gpio': 0,
        'voltage': 5,
        'notes': u'Some notes.',
        'description': u'The garage door.',
        'active': False,
        'open': False
    }
]

temps = [
    {
        'id': 1,
        'type': u'temp',
        'gpio': 0,
        'voltage': 5,
        'notes': u'Some notes.',
        'temp': 0,
        'description': u'Office temp.',
        'active': False
    }

]

motion_sensors = [
    {
        'id': 1,
        'type': u'sensor',
        'gpio': 0,
        'voltage': 5,
        'notes': u'Some notes.',
        'description': u'Office temp.',
        'active': False
    }
]

pi_nodes = [
    {
        'id': 1,
        'version': u'vB',   #vA, vB, vB+ 
        'notes': u'Some notes.',
        'cputemp': 0,
        'description': u'Garage pi-node.',
        'lastupdate': '0',
        'ip': '',
        'active': False
    }
]

pi_servers = [
    {
        'id': 1,
        'version': u'vB',   #vA, vB, vB+
        'notes': u'Some notes.',
        'cputemp': 0,
        'description': u'Central pi-server.',
        'lastupdate': '0',
        'ip': '',
        'active': False
    }
]


# ====================================================================
# IP logging
# ====================================================================
@app.route("/get_my_ip/", methods=["GET"])
def get_my_ip():
    print(request.remote_addr)
    return jsonify({'ip': request.remote_addr}), 200

# ====================================================================
# Doors 
# ====================================================================
@app.route('/api/doors/', methods = ['GET'])
@auth.login_required
def get_doors():
    return jsonify( { 'doors': doors } )

@app.route('/api/doors/<int:door_id>', methods = ['GET'])
@auth.login_required
def get_door_id(door_id):
    d_id = filter(lambda t: t['id'] == door_id, doors)
    if len(d_id ) == 0:
        abort(404)
    return jsonify( { 'door': d_id[0] } )

@app.route('/api/doors/', methods = ['POST'])
@auth.login_required
def create_door():
    if not request.json or not 'gpio' in request.json:
        abort(400)
    door = {
        'id': doors[-1]['id'] + 1,
        'type': request.json.get('type', ""),
        'gpio': request.json['gpio'],
        'voltage': request.json.get('voltage', ""),
        'notes': request.json.get('notes', ""),
        'description': request.json.get('description', ""),
        'active': False,
        'open': False
    }
    doors.append(door)
    return jsonify( { 'door': door } ), 201

@app.route('/api/doors/<int:door_id>', methods = ['PUT'])
@auth.login_required
def update_door(door_id):
    door = filter(lambda t: t['id'] == door_id, doors)
    if len(door) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'open' in request.json and type(request.json['open']) is not bool:
        abort(400)
    door[0]['type'] = request.json.get('type', door[0]['type'])
    door[0]['gpio'] = request.json.get('gpio', door[0]['gpio'])
    door[0]['voltage'] = request.json.get('voltage', door[0]['voltage'])
    door[0]['notes'] = request.json.get('notes', door[0]['notes'])
    door[0]['description'] = request.json.get('description', door[0]['description'])
    door[0]['open'] = request.json.get('open', door[0]['open'])
    return jsonify( { 'door': door[0] } )

@app.route('/api/doors/<int:door_id>', methods = ['DELETE'])
@auth.login_required
def delete_door(door_id):
    door = filter(lambda t: t['id'] == door_id, doors)
    if len(door) == 0:
        abort(404)
    doors.remove(door[0])
    return jsonify( { 'result': True } )

# ====================================================================
# Windows                     
# ====================================================================
@app.route('/api/windows/', methods = ['GET'])
@auth.login_required
def get_windows():
    return jsonify( { 'windows': windows } )

@app.route('/api/windows/<int:window_id>', methods = ['GET'])
@auth.login_required
def get_window_id(window_id):
    w_id = filter(lambda t: t['id'] == window_id, windows)
    if len(w_id) == 0:
        abort(404)
    return jsonify( { 'window': w_id[0] } )

@app.route('/api/windows/', methods = ['POST'])
@auth.login_required
def create_window():
    if not request.json or not 'gpio' in request.json:
        abort(400)
    window =  {
        'id': windows[-1]['id'] + 1,
        'type': request.json.get('type', ""),
        'gpio': request.json['gpio'],
        'voltage': request.json.get('voltage', ""),
        'notes': request.json.get('notes', ""),
        'description': request.json.get('description', ""),
        'open': False
    }
    windows.append(window)
    return jsonify( { 'window': window } ), 201

@app.route('/api/windows/<int:window_id>', methods = ['PUT'])
@auth.login_required
def update_window(window_id):
    window = filter(lambda t: t['id'] == window_id, windows)
    if len(window) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'open' in request.json and type(request.json['open']) is not bool:
        abort(400)
    window[0]['type'] = request.json.get('type', window[0]['type'])
    window[0]['gpio'] = request.json.get('gpio', window[0]['gpio'])
    window[0]['voltage'] = request.json.get('voltage', window[0]['voltage'])
    window[0]['notes'] = request.json.get('notes', window[0]['notes'])
    window[0]['description'] = request.json.get('description', window[0]['description'])
    window[0]['open'] = request.json.get('open', window[0]['open'])
    return jsonify( { 'window': window[0] } )

@app.route('/api/windows/<int:window_id>', methods = ['DELETE'])
@auth.login_required
def delete_window(window_id):
    window = filter(lambda t: t['id'] == window_id, windows)
    if len(window) == 0:
        abort(404)
    windows.remove(window[0])
    return jsonify( { 'result': True } )


# ====================================================================
# Garage Door                     
# ====================================================================
@app.route('/api/garage/', methods = ['GET'])
@auth.login_required
def get_garage():
    return jsonify( { 'garage': garage } )

@app.route('/api/garage/<int:garage_id>', methods = ['GET'])
@auth.login_required
def get_garage_id(garage_id):
    g_id = filter(lambda t: t['id'] == garage_id, garage)
    if len(g_id) == 0:
        abort(404)
    return jsonify( { 'garage': g_id[0] } )

@app.route('/api/garage/', methods = ['POST'])
@auth.login_required
def create_garage():
    if not request.json or not 'gpio' in request.json:
        abort(400)
    g_garage = {
        'id': garage[-1]['id'] + 1,
        'type': request.json.get('type', ""),
        'gpio': request.json['gpio'],
        'voltage': request.json.get('voltage', ""),
        'notes': request.json.get('notes', ""),
        'description': request.json.get('description', ""),
        'active': False,
        'open': False
    }

    garage.append(g_garage)
    return jsonify( { 'garage': g_garage } ), 201

@app.route('/api/garage/<int:garage_id>', methods = ['PUT'])
@auth.login_required
def update_garage(garage_id):
    g_garage = filter(lambda t: t['id'] == garage_id, garage)
    if len(g_garage) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'open' in request.json and type(request.json['open']) is not bool:
        abort(400)
    g_garage[0]['type'] = request.json.get('type', g_garage[0]['type'])
    g_garage[0]['gpio'] = request.json.get('gpio', g_garage[0]['gpio'])
    g_garage[0]['voltage'] = request.json.get('voltage', g_garage[0]['voltage'])
    g_garage[0]['notes'] = request.json.get('notes', g_garage[0]['notes'])
    g_garage[0]['description'] = request.json.get('description', g_garage[0]['description'])
    g_garage[0]['open'] = request.json.get('open', g_garage[0]['open'])
    return jsonify( { 'garage': g_garage[0] } )

@app.route('/api/garage/<int:garage_id>', methods = ['DELETE'])
@auth.login_required
def delete_garage(garage_id):
    g_garage = filter(lambda t: t['id'] == garage_id, garage)
    if len(g_garage) == 0:
        abort(404)
    garage.remove(g_garage[0])
    return jsonify( { 'result': True } )

# ====================================================================
# Temps
# ====================================================================
@app.route('/api/temps/', methods = ['GET'])
@auth.login_required
def get_temps():
    return jsonify( { 'temps': temps } )

@app.route('/api/temps/<int:temp_id>', methods = ['GET'])
@auth.login_required
def get_temp_id(temp_id):
    t_id = filter(lambda t: t['id'] == temp_id, temps)
    if len(t_id) == 0:
        abort(404)
    return jsonify( { 'temp': t_id[0] } )

@app.route('/api/temps/', methods = ['POST'])
@auth.login_required
def create_temp():
    if not request.json or not 'gpio' in request.json:
        abort(400)
    temp = {
        'id': temps[-1]['id'] + 1,
        'type': request.json.get('type', ""),
        'gpio': request.json['gpio'],
        'voltage': request.json.get('voltage', ""),
        'notes': request.json.get('notes', ""),
        'temp': request.json.get('temp', ""),
        'description': request.json.get('description', ""),
        'active': False
    }

    temps.append(temp)
    return jsonify( { 'temp': temp } ), 201

@app.route('/api/temps/<int:temp_id_put>', methods = ['PUT'])
@auth.login_required
def update_temp(temp_id_put):
    temp = filter(lambda t: t['id'] == temp_id_put, temps)
    if len(temp) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'open' in request.json and type(request.json['open']) is not bool:
        abort(400)
    temp[0]['type'] = request.json.get('type', temp[0]['type'])
    temp[0]['gpio'] = request.json.get('gpio', temp[0]['gpio'])
    temp[0]['voltage'] = request.json.get('voltage', temp[0]['voltage'])
    temp[0]['notes'] = request.json.get('notes', temp[0]['notes'])
    temp[0]['temp'] = request.json.get('temp', temp[0]['temp'])
    temp[0]['description'] = request.json.get('description', temp[0]['description'])
    temp[0]['active'] = request.json.get('active', temp[0]['active'])
    return jsonify( { 'temp': temp[0] } )

@app.route('/api/temps/<int:temp_id_del>', methods = ['DELETE'])
@auth.login_required
def delete_temp(temp_id):
    temp = filter(lambda t: t['id'] == temp_id_del, temps)
    if len(temp) == 0:
        abort(404)
    temps.remove(temp[0])
    return jsonify( { 'result': True } )

# ====================================================================
# Motion Sensors
# ====================================================================
@app.route('/api/motions/', methods = ['GET'])
@auth.login_required
def get_motions():
    return jsonify( { 'motions': motion_sensors } )

@app.route('/api/motions/<int:motion_id>', methods = ['GET'])
@auth.login_required
def get_motion_id(motion_id):
    motion = filter(lambda t: t['id'] == motion_id, motion_sensors)
    if len(motion) == 0:
        abort(404)
    return jsonify( { 'motion': motion[0] } )

@app.route('/api/motions/', methods = ['POST'])
@auth.login_required
def create_motion():
    if not request.json or not 'gpio' in request.json:
        abort(400)
    motion =  {
        'id': motion_sensors[-1]['id'] + 1,
        'type': request.json.get('type', ""),
        'gpio': request.json['gpio'],
        'voltage': request.json.get('voltage', ""),
        'notes': request.json.get('notes', ""),
        'description': request.json.get('description', ""),
        'active': False
    }
    motion_sensors.append(motion)
    return jsonify( { 'motion': motion } ), 201

@app.route('/api/motions/<int:motion_id>', methods = ['PUT'])
@auth.login_required
def update_motion(motion_id):
    motion = filter(lambda t: t['id'] == motion_id, motion_sensors)
    if len(motion) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'open' in request.json and type(request.json['open']) is not bool:
        abort(400)
    motion[0]['type'] = request.json.get('type', motion[0]['type'])
    motion[0]['gpio'] = request.json.get('gpio', motion[0]['gpio'])
    motion[0]['voltage'] = request.json.get('voltage', motion[0]['voltage'])
    motion[0]['notes'] = request.json.get('notes', motion[0]['notes'])
    motion[0]['description'] = request.json.get('description', motion[0]['description'])
    motion[0]['active'] = request.json.get('active', motion[0]['active'])
    return jsonify( { 'motion': motion[0] } )

@app.route('/api/motions/<int:motion_id>', methods = ['DELETE'])
@auth.login_required
def delete_motion(motion_id):
    motion = filter(lambda t: t['id'] == motion_id, motion_sensors)
    if len(motion) == 0:
        abort(404)
    motion_sensors.remove(motion[0])
    return jsonify( { 'result': True } )

# ====================================================================
# pi_nodes
# ====================================================================
@app.route('/api/nodes/', methods = ['GET'])
@auth.login_required
def get_nodes():
    return jsonify( { 'nodes': pi_nodes } )

@app.route('/api/nodes/<int:node_id>', methods = ['GET'])
@auth.login_required
def get_node_id(node_id):
    n_id = filter(lambda t: t['id'] == node_id, pi_nodes)
    if len(n_id ) == 0:
        abort(404)
    return jsonify( { 'node': n_id[0] } )

@app.route('/api/nodes/', methods = ['POST'])
@auth.login_required
def create_node():
    node = {
        'id': pi_nodes[-1]['id'] + 1,
        'version': request.json.get('type', ""),
        'notes': request.json.get('notes', ""),
        'cputemp': 0,
        'description': request.json.get('description', ""),
        'lastupdate': request.json.get('lastupdate', ""),
        'ip': request.remote_addr,
        'active': False
    }
    pi_nodes.append(node)
    return jsonify( { 'node': node } ), 201

@app.route('/api/nodes/<int:node_id>', methods = ['PUT'])
@auth.login_required
def update_node(node_id):
    node = filter(lambda t: t['id'] == node_id, pi_nodes)
    if len(node) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'open' in request.json and type(request.json['open']) is not bool:
        abort(400)
    node[0]['version'] = request.json.get('version', node[0]['version'])
    node[0]['notes'] = request.json.get('notes', node[0]['notes'])
    node[0]['cputemp'] = request.jason.get('cputemp', node[0]['cputemp'])
    node[0]['description'] = request.json.get('description', node[0]['description'])
    node[0]['active'] = request.json.get('open', node[0]['active'])
    #node[0]['ip'] = request.remote_addr
    return jsonify( { 'node': node[0] } )

@app.route('/api/nodes/<int:node_id>', methods = ['DELETE'])
@auth.login_required
def delete_node(node_id):
    node = filter(lambda t: t['id'] == node_id, pi_nodes)
    if len(node) == 0:
        abort(404)
    pi_nodes.remove(node[0])
    return jsonify( { 'result': True } )


# ====================================================================
# pi_servers
# ====================================================================
@app.route('/api/servers/', methods = ['GET'])
@auth.login_required
def get_servers():
    return jsonify( { 'servers': pi_servers } )

@app.route('/api/servers/<int:server_id>', methods = ['GET'])
@auth.login_required
def get_server_id(server_id):
    n_id = filter(lambda t: t['id'] == server_id, pi_servers)
    if len(n_id ) == 0:
        abort(404)
    return jsonify( { 'server': n_id[0] } )

@app.route('/api/servers/', methods = ['POST'])
@auth.login_required
def create_server():
    server = {
        'id': pi_servers[-1]['id'] + 1,
        'version': request.json.get('version', ""),
        'notes': request.json.get('notes', ""),
        'cputemp': request.json.get('cputemp', ""), 
        'description': request.json.get('description', ""),
        'lastupdate': request.json.get('lastupdate', ""),
        'ip': request.remote_addr,
        'active': False
    }
    pi_servers.append(server)
    return jsonify( { 'server': server } ), 201

@app.route('/api/servers/<int:server_id>', methods = ['PUT'])
@auth.login_required
def update_server(server_id):
    server = filter(lambda t: t['id'] == server_id, pi_servers)
    if len(server) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'open' in request.json and type(request.json['open']) is not bool:
        abort(400)
    server[0]['version'] = request.json.get('version', server[0]['version'])
    server[0]['notes'] = request.json.get('notes', server[0]['notes'])
    server[0]['cputemp'] = request.json.get('cputemp', server[0]['cputemp'])
    server[0]['description'] = request.json.get('description', server[0]['description'])
    server[0]['active'] = request.json.get('active', server[0]['active'])
    #server[0]['ip'] = request.remote_addr
    return jsonify( { 'server': server[0] } )

@app.route('/api/servers/<int:server_id>', methods = ['DELETE'])
@auth.login_required
def delete_server(server_id):
    server = filter(lambda t: t['id'] == server_id, pi_servers)
    if len(server) == 0:
        abort(404)
    pi_servers.remove(server[0])
    return jsonify( { 'result': True } )



# ====================================================================
# Error Handling
# ====================================================================
@app.errorhandler(404)
def not_found(error):
    return make_response( jsonify( { 'error': 'Not found' } ), 404 )

# ====================================================================
# Main function
# ====================================================================
if __name__ == '__main__':
    print ("Starting Flask \n")
    print doors
    app.run(host='0.0.0.0')

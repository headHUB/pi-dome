#!/usr/bin/python
import httplib
import base64
import string
import json
def post(base, port, url, payload):
	conn = httplib.HTTPConnection(base, port, timeout=60)
	#conn.request('POST', url, payload, { 'Authorization' : 'Basic '+string.strip(base64.encodestring('pi-dome:pi-dome')), 'Content-Type' : 'application/json' })
	conn.request('PUT', url, payload, { 'Authorization' : 'Basic '+string.strip(base64.encodestring('pi-dome:pi-dome')), 'Content-Type' : 'application/json' })
	r = conn.getresponse()
	return r.read()

# Note that json.dumps may also be used to create the json string from a python object
to_write = '{    "192.168.1.100": {        "1": {            "gpio_setting": "3v",            "active": false,            "type": "3v",            "action": "<script>",            "description": "Woos! POOSH The GPIO outputs continuous 3 volts."        },        "2": {            "gpio_setting": "5v",            "active": false,            "type": "5v",            "action": "<script>",            "description": "The GPIO outputs continuous 5 volts."        },        "3": {            "gpio_setting": "I2c",            "active": false,            "type": "<door|window|action|motion_sensor>",            "action": "/some/script/to/run",            "description": "This is a I2C GPIO and always outputs."        },        "4": {            "gpio_setting": "5v",            "active": false,            "type": "5v",            "action": "<script>",            "description": "The GPIO outputs continuous 5 volts."        },        "5": {            "gpio_setting": "I2c",            "active": false,            "type": "<door|window|action|motion_sensor>",            "action": "",            "description": "This is a I2C GPIOi and always outputs."        },        "6": {            "gpio_setting": "Ground",            "active": false,            "type": "Ground",            "action": "<script>",            "description": "The GPIO is for ground."        },        "7": {            "gpio_setting": "PUD_DOWN",            "active": false,            "type": "<door|window|action|motion_sensor>",            "action": "",            "description": "This is a GPIO."        },        "8": {            "gpio_setting": "PUD_DOWN",            "active": false,            "type": "<door|window|action|motion_sensor>",            "action": "",            "description": "This is a GPIO."        },        "9": {            "gpio_setting": "Ground",            "active": false,            "type": "Ground",            "action": "<script>",            "description": "The GPIO is for ground."        },        "10": {            "gpio_setting": "PUD_DOWN",            "active": false,            "type": "<door|window|action|motion_sensor>",            "action": "",            "description": "This is a GPIO."        },        "11": {            "gpio_setting": "PUD_DOWN",            "active": false,            "type": "<door|window|action|motion_sensor>",            "action": "",            "description": "This is a GPIO."        },        "12": {            "gpio_setting": "PUD_DOWN",            "active": false,            "type": "<door|window|action|motion_sensor>",            "action": "",            "description": "This is a GPIO."        },        "13": {            "gpio_setting": "PUD_DOWN",            "active": false,            "type": "<door|window|action|motion_sensor>",            "action": "",            "description": "This is a GPIO."        },        "14": {            "gpio_setting": "Ground",            "active": false,            "type": "Ground",            "action": "<script>",            "description": "The GPIO is for ground."        },        "15": {            "gpio_setting": "PUD_DOWN",            "active": false,            "type": "<door|window|action|motion_sensor>",            "action": "",            "description": "This is a GPIO."        },        "16": {            "gpio_setting": "PUD_DOWN",            "active": false,            "type": "<door|window|action|motion_sensor>",            "action": "",            "description": "This is a GPIO."        },        "17": {            "gpio_setting": "3v",            "active": false,            "type": "3v",            "action": "<script>",            "description": "The GPIO delivers 3v continuously."        },        "18": {            "gpio_setting": "PUD_DOWN",            "active": false,            "type": "<door|window|action|motion_sensor>",            "action": "",            "description": "This is a GPIO."        },        "19": {            "gpio_setting": "PUD_DOWN",            "active": false,            "type": "<door|window|action|motion_sensor>",            "action": "",            "description": "This is a GPIO."        },        "20": {            "gpio_setting": "Ground",            "active": false,            "type": "Ground",            "action": "<script>",            "description": "The GPIO is for ground."        },        "21": {            "gpio_setting": "PUD_DOWN",            "active": false,            "type": "<door|window|action|motion_sensor>",            "action": "",            "description": "This is a GPIO."        },        "22": {            "gpio_setting": "PUD_DOWN",            "active": false,            "type": "<door|window|action|motion_sensor>",            "action": "",            "description": "This is a GPIO."        },        "23": {            "gpio_setting": "PUD_DOWN",            "active": false,            "type": "<door|window|action|motion_sensor>",            "action": "",            "description": "This is a GPIO."        },        "24": {            "gpio_setting": "PUD_DOWN",            "active": false,            "type": "<door|window|action|motion_sensor>",            "action": "",            "description": "This is a GPIO."        },        "25": {            "gpio_setting": "Ground",            "active": false,            "type": "Ground",            "action": "<script>",            "description": "The GPIO is for ground."        },        "26": {            "gpio_setting": "PUD_DOWN",            "active": false,            "type": "<door|window|action|motion_sensor>",            "action": "",            "description": "This is a GPIO."        },        "27": {            "gpio_setting": "DNC",            "active": false,            "type": "DNC",            "action": "<script>",            "description": "DO NOT CONNECT!"        },        "28": {            "gpio_setting": "DNC",            "active": false,            "type": "DNC",            "action": "<script>",            "description": "DO NOT CONNECT!"        },        "29": {            "gpio_setting": "PUD_DOWN",            "active": false,            "type": "<door|window|action|motion_sensor>",            "action": "",            "description": "This is a GPIO."        },        "30": {            "gpio_setting": "Ground",            "active": false,            "type": "Ground",            "action": "<script>",            "description": "The GPIO is for ground."        },        "31": {            "gpio_setting": "PUD_DOWN",            "active": false,            "type": "<door|window|action|motion_sensor>",            "action": "",            "description": "This is a GPIO."        },        "32": {            "gpio_setting": "PUD_DOWN",            "active": false,            "type": "<door|window|action|motion_sensor>",            "action": "",            "description": "This is a GPIO."        },        "33": {            "gpio_setting": "PUD_DOWN",            "active": false,            "type": "<door|window|action|motion_sensor>",            "action": "",            "description": "This is a GPIO."        },        "34": {            "gpio_setting": "Ground",            "active": false,            "type": "Ground",            "action": "<script>",            "description": "The GPIO is for ground."        },        "35": {            "gpio_setting": "PUD_DOWN",            "active": false,            "type": "<door|window|action|motion_sensor>",            "action": "",            "description": "This is a GPIO."        },        "36": {            "gpio_setting": "PUD_DOWN",            "active": false,            "type": "<door|window|action|motion_sensor>",            "action": "",            "description": "This is a GPIO."        },        "37": {            "gpio_setting": "PUD_DOWN",            "active": false,            "type": "<door|window|action|motion_sensor>",            "action": "",            "description": "This is a GPIO."        },        "38": {            "gpio_setting": "PUD_DOWN",            "active": false,            "type": "<door|window|action|motion_sensor>",            "action": "",            "description": "This is a GPIO."        },        "39": {            "gpio_setting": "Ground",            "active": false,            "type": "Ground",            "action": "<script>",            "description": "The GPIO is for ground."        },        "40": {            "gpio_setting": "PUD_DOWN",            "active": false,            "type": "<door|window|action|motion_sensor>",            "action": "",            "description": "This is a GPIO."        }    }} '

try:
    data = post("vengersonline.com", 5000, "/api/nodes/192.168.1.100", to_write)
    #data = post("vengersonline.com", 5000, "/api/nodes/", to_write)
    print json.loads(data)
except:
    print ("fail")


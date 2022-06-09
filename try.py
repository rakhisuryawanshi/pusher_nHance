import gzip
import json
from base64 import b64decode
from pprint import pprint
from time import sleep

import requests
from pysher import Pusher

CHANNEL = 'private-location-208'
AUTH_URI = 'https://eu-api.empathicbuilding.com/v1/pusher/auth'
AUTH_HEADERS = {'authorization': 'Bearer d689be5d-0333-4af8-b8dc-aac119870578'}  # replace this


def print_json(data):
    uncompressed = gzip.decompress(b64decode(data))
    json_data = json.loads(uncompressed)
    pprint(json_data)


def connect_handler(data):
    # Get the authorization token from the EB server
    print("Here i am")
    data = json.loads(data)
    form = {'channel_name': CHANNEL, 'socket_id': data['socket_id']}
    response = requests.post(AUTH_URI, data=form, headers=AUTH_HEADERS)
    response.raise_for_status()
    token = response.json()['auth']
    # Subscribe to the channel
    chan = pusher.subscribe(CHANNEL, auth=token)

    # Add an event handler for "sensor-modified" events
    chan.bind('sensor-modified', print_json)

pusher = Pusher('33d6c4f799c274f7e0bc', cluster='eu', log_level=None)
channel = pusher.subscribe(CHANNEL)
channel.bind('pusher:connection_established', connect_handler)
# pusher.connect()
while True:
    sleep(1)
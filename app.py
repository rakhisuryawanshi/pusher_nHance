import json
import yaml
import os
import sys
from pprint import pprint 
from time import sleep
from base64 import b64decode
import gzip
import requests
from pysher import Pusher
import logging.config

logger = logging.getLogger(__name__)

def config(config_file=None):
    """Get config from file; if no config_file is passed in as argument  default to "config.yaml" in script dir"""
    if config_file is None:
        script_base_dir = os.path.dirname(os.path.realpath(sys.argv[0])) + "/"
        config_file = script_base_dir + "config.yaml"
    with open(config_file, 'r') as stream:
        return yaml.load(stream,Loader=yaml.FullLoader)


def handle_message(data):
    decoded = b64decode(data)
    decompressed = gzip.decompress(decoded)
    json_data = json.loads(decompressed.decode('utf-8'))

    for sensor in json_data:
        logger.info(sensor)  



def connect_handler(data):
    # Get the authorization token from the EB server
    data = json.loads(data)
    headers = {'authorization': "Bearer 0b910e00-f6d8-4b5d-bb43-5906743970ff"}
    form = {'channel_name': channel, 'socket_id': data['socket_id']}
    response = requests.post(api_url, data=form, headers=headers)
    response.raise_for_status()
    token = response.json()['auth']

    # Subscribe to the channel
    chan = pusher.subscribe(channel, auth=token)

    # Add an event handler for "sensor-modified" events
    chan.bind('sensor-modified', handle_message)
    logger.info('Connected to Pusher.com and subscribed to channel "sensor-modified" ')


if __name__ == "__main__":
    try:
        config = config(config_file=sys.argv[1])
    except IndexError:
        config = config()

    if "logging" in config:
        log_config = config["logging"]
        logging.config.dictConfig(log_config)
    if "eb" in config:
        api_url = config["eb"]["api_url"]
        access_token = config["eb"]["access_token"]
        asset_api_url = config["eb"]["asset_api_url"]
    if "pusher" in config:
        channel = config["pusher"]["channel"]
        key = config["pusher"]["key"]
        cluster = config["pusher"]["cluster"]

    headers = {'content-type': 'application/json', 'Authorization':  'Bearer ' + access_token }

    pusher = Pusher(key, cluster=cluster, log_level=logging.ERROR)
    pusher.connection.bind('pusher:connection_established', connect_handler)
    pusher.connect()
    while True:
        sleep(1)

import sys
import time
import pysher

# Add a logging handler so we can see the raw communication data
import logging

root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
root.addHandler(ch)

pusher = pysher.Pusher('64737761a47148863544')


def my_func(*args, **kwargs):
 print("processing Args:", args)
 print("processing Kwargs:", kwargs)


# We can't subscribe until we've connected, so we use a callback handler
# to subscribe when able
def connect_handler(data):
 channel = pusher.subscribe('private-location-208')
 channel.bind('myevent', my_func)


pusher.connection.bind('pusher:connection_established', connect_handler)
pusher.connect()

while True:
 # Do other things in the meantime here...
 time.sleep(1)
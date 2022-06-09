import datetime

import requests

AUTH_HEADERS = {'authorization': 'Bearer b46b935b-5cc7-4d17-9691-7b7f64b13b37'}  # replace this

d1 = datetime.datetime.now()
now_milliseconds = int(d1.timestamp() * 1000)
valid_to = now_milliseconds + 15 * 60000  # 15 minutes
data = [
    {'vendor_id': 'ABC-123', 'time': now_milliseconds, 'valid_to': valid_to,
     'type': 'temperature', 'value': 23.756}
]
response = requests.post('https://eu-api.empathicbuilding.com/v2/measurements', json=data,
                         headers=AUTH_HEADERS)
response.raise_for_status()
# -----------------------------------------------------------------------------------------------
#
#       Company:    Personal Research
#       By:         Fredrick Stakem
#       Created:    7.3.17   
#
# -----------------------------------------------------------------------------------------------


# Libraries
import requests
import time
import json


important_urls = [
    'http://hassbian.local:8123/api',
    'http://hassbian.local:8123/api/config',
    'http://hassbian.local:8123/api/discovery_info',
    'http://hassbian.local:8123/api/states/sensor.nodemcu_1'
]

# yr_symbol

# select * from states where entity_id='sensor.nodemcu_1';

#   {
#       'attributes': {'friendly_name': 'Nodemcu 1'},
#       'entity_id': 'sensor.nodemcu_1',
#       'last_changed': '2017-06-24T13:49:24.444437+00:00',
#       'last_updated': '2017-06-24T13:49:24.444437+00:00',
#       'state': 'unknown'
#   }


while False:
    url = "http://hassbian.local:8123/api/states/sensor.yr_symbol"

    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        'X-HA-Access': "raspberry"
    }

    response = requests.request("GET", url, headers=headers)
    states = json.loads(response.text)

    for state in states:
        name = state['attributes']['friendly_name']
        entity_id = state['entity_id']
        timestamp = state['last_updated']
        state_value = state['state']

    print(response.text)

    sleep_time_sec = 60 * 5
    time.sleep(sleep_time_sec)


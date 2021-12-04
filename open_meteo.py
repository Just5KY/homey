import requests
import json
from secretKeys import weatherLat, weatherLong

# https://open-meteo.com/en/docs

CONFIG_STRING = '/v1/forecast?latitude=' + weatherLat + '&longitude=' + weatherLong + '&hourly=temperature_2m,precipitation,weathercode,snow_height&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch&timezone=America%2FNew_York&past_days=2'

class api:

    def __init__(self, host, verbose=False):
        self.host = host
        self.verbose = verbose

    def request(self, method, path, query, body):
        url = self.host + path
        if query:
            url += '?' + query

        if self.verbose:
            print(method, url)

        s = requests.Session()
        if body:
            body_json = json.dumps(body)
            response = s.request(method, url, data=body_json)
        else:
            response = s.request(method, url)

        if response.status_code == 200:
            return response.json()
        elif response.content:
            raise Exception(str(response.status_code) + ": " + response.reason + ": " + str(response.content))
        else:
            raise Exception(str(response.status_code) + ": " + response.reason)

    def get_all_weather_data(self):
        return self.request('GET', CONFIG_STRING, '', None)

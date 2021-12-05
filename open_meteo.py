import requests
import json
from datetime import datetime
from secretKeys import weatherLat, weatherLong
from weatherCodes import WEATHER_CODES

# https://open-meteo.com/en/docs
API_DAYS = 7
API_HOURS = 168

class api:

    def buildUrl(self, params):
        return 'https://api.open-meteo.com/v1/forecast?latitude=' + weatherLat + '&longitude=' + weatherLong \
            + params + '&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch&timezone=America%2FNew_York'
    
    def request(self, method, url):
        s = requests.Session()
        response = s.request(method, url)

        if response.status_code == 200:
            return response.json()
        elif response.content:
            raise Exception(str(response.status_code) + ": " + response.reason + ": " + str(response.content))
        else:
            raise Exception(str(response.status_code) + ": " + response.reason)

    def getWeatherWeekly(self):
        dailyData = []
        response = self.request('GET', self.buildUrl('&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum'))['daily']

        for i in range(API_DAYS):
            dailyData.append({
                'day': response['time'][i],
                'weather_type': WEATHER_CODES[response['weathercode'][i]],
                'temp_min': response['temperature_2m_min'][i],
                'temp_max': response['temperature_2m_max'][i],
                'precipitation': response['precipitation_sum'][i]
            })

        return dailyData

    def getWeatherHourly(self, day=''):
        hourlyData = []
        response = self.request('GET', self.buildUrl('&hourly=temperature_2m,precipitation,weathercode,snow_depth'))['hourly']

        # Get 24 hours of weather for a specific day
        if day != '':
            dayOffset = int(day[-2:]) - int(datetime.today().strftime('%Y%m%d')[-2:])
            startHr = dayOffset * 24
            for i in range(startHr, startHr + 24):
                hourlyData.append({
                    'time': response['time'][i],
                    'weather_type': WEATHER_CODES[response['weathercode'][i]],
                    'temp': response['temperature_2m'][i],
                    'snow_depth': response['snow_depth'][i],
                    'precipitation': response['precipitation'][i]
                })

        # Get 168 hours of weather for the next 7 days
        else:
            for i in range(API_HOURS):
                hourlyData.append({
                    'time': response['time'][i],
                    'weather_type': WEATHER_CODES[response['weathercode'][i]],
                    'temp': response['temperature_2m'][i],
                    'snow_depth': response['snow_depth'][i],
                    'precipitation': response['precipitation'][i]
                })

        return hourlyData

import requests
import json
from datetime import datetime
from dateutil.parser import parse

# https://open-meteo.com/en/docs
API_DAYS = 7
API_HOURS = 168

WEATHER_CODES = {
  0: 'Clear',
  1: 'Mostly Clear',
  2: 'Partly Cloudy',
  3: 'Overcast',
  45: 'Fog',
  48: 'Depositing rime fog',
  51: 'Light Drizzle',
  53: 'Moderate Drizzle',
  55: 'Heavy Drizzle',
  56: 'Light Freezing Drizzle',
  57: 'Heavy Freezing Drizzle',
  61: 'Light Rain',
  63: 'Rain',
  65: 'Heavy Rain',
  66: 'Light Freezing Rain',
  67: 'Heavy Freezing Rain',
  71: 'Light Snow',
  73: 'Moderate Snow',
  75: 'Heavy Snow',
  77: 'Snow Grains',
  80: 'Light Showers',
  81: 'Moderate Showers',
  82: 'Heavy Showers',
  85: 'Light Snow Showers',
  86: 'Heavy Snow Showers',
  95: 'Thunderstorm',
  96: 'Light Thunderstorm w/ Hail',
  99: 'Heavy Thunderstorm w/ Hail'
}

class api:

    def __init__(self, weatherLat, weatherLong):

        self.weatherLat = weatherLat
        self.weatherLong = weatherLong

    def buildUrl(self, params):
        return 'https://api.open-meteo.com/v1/forecast?latitude=' + self.weatherLat + '&longitude=' + self.weatherLong \
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
                'day': datetime.strptime(response['time'][i], '%Y-%m-%d').strftime('%A, %b %-m'),
                'weekday': 'Today' if i == 0 else datetime.strptime(response['time'][i], '%Y-%m-%d').strftime('%A'),
                'weather_type': WEATHER_CODES[response['weathercode'][i]],
                'temp_min': int(round(response['temperature_2m_min'][i])),
                'temp_max': int(round(response['temperature_2m_max'][i])),
                'precipitation': response['precipitation_sum'][i]
            })

        return dailyData

    def getWeatherHourly(self, day=''):
        hourlyData = []
        response = self.request('GET', self.buildUrl('&hourly=temperature_2m,precipitation,weathercode,snow_depth'))['hourly']

        # Get 24 hours of weather for a specific day within the 7 day forecast
        if day != '':
            startHr = 0
            dayOffset = int(day[-2:]) - datetime.today().day
            if dayOffset == 0: # If getting data for the current day, start at the current hour
                startHr = (dayOffset * 24) + datetime.today().hour
                
            for i in range(startHr, startHr + 24):
                hourlyData.append({
                    'time': parse(response['time'][i]).strftime("%-I %p"),
                    'weather_type': WEATHER_CODES[response['weathercode'][i]],
                    'temp': int(round(response['temperature_2m'][i])),
                    'snow_depth': response['snow_depth'][i],
                    'precipitation': response['precipitation'][i]
                })

        # Get 168 hours of weather for the next 7 days
        else:
            for i in range(API_HOURS):
                hourlyData.append({
                    'time': parse(response['time'][i]).strftime("%m/%d %-I %p"),
                    'weather_type': WEATHER_CODES[response['weathercode'][i]],
                    'temp': int(round(response['temperature_2m'][i])),
                    'snow_depth': response['snow_depth'][i],
                    'precipitation': response['precipitation'][i]
                })

        return hourlyData

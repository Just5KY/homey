# homey-server

Backend server in flask for homey dashboard. Mostly used to fetch API data.

## Documentation
The backend runs on port 9101 by default. For example, to get JSON-formatted hourly weather for March 12th 2021:
    
    GET http://0.0.0.0:9101/weatherHourly/20210312

Weather location, timezone, and portainer API information can be configured in `secretKeys.py`.

### weatherWeekly
Get 7 days of daily weather forecast data, beginning at the current day.

    "day": "2021-12-05"
    "precipitation": 0.1
    "temp_max": 35.8
    "temp_min": 30.5
    "weather_type": "Light Snow Showers"

### weatherHourly
Get 168 hours (7 days) of hourly weather forecast data, beginning at midnight of the current day in the configured timezone. Each hour is formatted as follows:

    "precipitation": 0.002
    "snow_depth": 0
    "temp": 42.8
    "time": "12/06 6 AM"
    "weather_type": "Overcast"

### weatherHourly/\<YYYYMMDD\>
Get 24 hours of hourly forecast data, beginning at midnight of the specified day in the configured timezone. If the current day is specified, the 24 hour window will begin at the start of the current hour.

    "precipitation": 0.048
    "snow_depth": 0
    "temp": 51.7
    "time": "4 PM"
    "weather_type": "Light Rain"

### portainerAuth
Attempt to authenticate the server with a local portainer API. Specify host, port, username, and password in `secretKeys.py`. Returns `True` if successful or already authenticated and `False` if the portainer API is unreachable or login information incorrect.

### portainerList
Returns a list of all running docker containers and their uptime as reported by portainer.

    {
        "name": "nextcloud"
        "status": "running"
        "uptime": "up 6 days"
    },
    {
        "name": "vaultwarden"
        "status": "running"
        "uptime": "up 2 hours"
    },
    ...



## Requirements
* python 3
* flask
* flask-cors

### Optional
* portainer (docker integration)
## Project setup & configuration
*If using private or location-based APIs: fill out `secretKeys.example.py` with your private information, then rename to `secretKeys.py`*

`pip install flask flask-cors`

`python app.py`
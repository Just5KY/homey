# homey-server

Backend server in flask for [homey dashboard](https://github.com/vlfldr/homey). Mostly used to fetch API data.

## Documentation
The backend runs on port 9101 by default. For example, to get JSON-formatted hourly weather for March 12th 2021:
    
    GET http://0.0.0.0:9101/weatherHourly/20210312

Weather location, timezone, and Portainer API information can be configured in `secretKeys.py`.

### weatherWeekly
Get 7 days of daily weather forecast data, beginning at the current day. Each day is formatted as follows:

    "day": "2021-12-05",
    "precipitation": 0.1,
    "temp_max": 35.8,
    "temp_min": 30.5,
    "weather_type": "Light Snow Showers"

### weatherHourly
Get 168 hours (7 days) of hourly weather forecast data, beginning at midnight of the current day in the configured timezone. Each hour is formatted as follows:

    "precipitation": 0.002,
    "snow_depth": 0,
    "temp": 42.8,
    "time": "12/06 6 AM",
    "weather_type": "Overcast"

### weatherHourly/\<YYYYMMDD\>
Get 24 hours of hourly forecast data, beginning at midnight of the specified day in the configured timezone. **The day must be in the forecast (i.e. current day - 7 days in the future).** If the current day is specified, the 24 hour window will begin at the start of the current hour.

    "precipitation": 0.048,
    "snow_depth": 0,
    "temp": 51.7,
    "time": "4 PM",
    "weather_type": "Light Rain"

*Note: Portainer and Docker backends are interchangeable. Configure in the dashboard's `config.yml` file. Portainer may provide more security and allows for easy remote management without exposing unsafe interfaces.*

### portainerAuth
Attempt to authenticate the server with a local Portainer API. Specify host, port, username, and password in `secretKeys.py`. Returns `True` if successful or already authenticated and `False` if the Portainer API is unreachable or login information incorrect.

### portainerList
Returns a list of all running docker containers and their uptime as reported by Portainer. Will attempt to `portainerAuth` if not already authenticated. Each container is formatted as follows:

        "name": "nextcloud",
        "status": "running",
        "uptime": "up 6 days"

### portainerControl/\<containerName\>/\<operation\>
Executes specified operation on specified container through Portainer. Valid operations: pause, unpause, start, stop, restart, kill. Will attempt to `portainerAuth` if not already authenticated. Returns an error if the container name is not found or the operation is not successful. Returns `success` if successful.

### dockerAuth
TODO: write about socket configuration

### dockerList
Returns a list of all running Docker containers and their uptime as reported by the local Docker instance's API. Each container is formatted as follows:

        "name": "nextcloud",
        "status": "running",
        "uptime": "up 6 days"

### dockerControl/\<containerName\>/\<operation\>
Executes specified operation on specified container through the Docker API. Valid operations: pause, unpause, start, stop, restart, kill. Returns an error if the container name is not found or the operation is not successful. Returns `success` if successful.

### floodAuth
Attempts to authenticate the server with a local Flood API. Specify host, port, username, and password in `secretKeys.py`. Returns `True` if successful or already authenticated and `False` if the Flood API is unreachable or login information incorrect.

### floodStats
Gets current upload/download speed and daily upload/downloaded data as reported by Flood. Will attempt to `floodAuth` if not already authenticated. Returns four values:

        "dailyDownloaded": "888mb",
        "dailyUploaded": "3.8gb",
        "downSpeed": "2.3mb/s",
        "upSpeed": "154kb/s"

### floodNotifications
Gets a list of all 'torrent finished' notifications from Flood. Each notification contains the torrent's name and the time it completed:

        "msg": "Nils Frahm - Old Friends New Friends (2021) - WEB FLAC",
        "time": "12/08 8:23 AM"

## Project setup & configuration

### Requirements
* python 3
* flask
* flask-cors

### Optional
* [Docker](https://docker.com)
* [Portainer](https://github.com/portainer/portainer) (Docker integration)
* [Flood](https://github.com/jesec/flood/) (torrent integration)

You can run homey, Portainer, and Flood side-by-side in Docker. A Docker image and user-friendly configuration will be provided upon project release. In the meantime, or if you want to run the backend locally or hack on it:

1. `git clone https://github.com/vlfldr/homey-server`

2. **Fill out `secretKeys.example.py` with your private information and rename to `secretKeys.py`.**

3. If you're using Portainer as a Docker backend, make sure homey can see port 9000 wherever Portainer is running (map 9000:9000 if running Portainer via docker)

4. If you're using the local Docker API backend, verify docker.sock exists at the location specified in `secretKeys.py`. If running Homey in Docker, map /var/run/docker.sock:/var/run/docker.sock so Homey can communicate with the parent Docker process. *Docker API backend can be specified in config.yml in homey*

5. If integrating with Flood, make sure homey can see Flood wherever the web UI is running (no additional mapping required)

6. `cd homey-server`

7. `pip install docker flask flask-cors`

8. `python app.py`

[homey](https://github.com/vlfldr/homey) should now be able to talk to the homey-server backend through port 9101.
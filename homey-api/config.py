import os
from dotenv import load_dotenv
import sys

### See config.yml for frontend config and .env for backend ###
################## DO NOT MODIFY THIS FILE ####################

# ensure config values are valid
def validateWeather(lat, long):
    try:
        fLat = float(lat)
        fLong = float(long)
    except ValueError:
        print('Error: WEATHER_LAT and WEATHER_LONG must be floats (XX.XXXX)')
        return False
    
    if fLat < -90 or fLat > 90:
        print('Error: WEATHER_LAT must be a valid latitude coordinate (-90.0000 - 90.0000)')
        return False
    if fLong < -180 or fLong > 180:
        print('Error: WEATHER_LONG must be a valid longitude coordinate (-180.0000 - 180.0000)')
        return False

    return True

class Config:
    RUNNING_IN_DOCKER = os.environ.get('HOMEY_API_RUNNING_IN_DOCKER', default='False').lower() == 'true'

    UPLOAD_FOLDER = './config/icons'

    # if running on metal, load .env file from project root
    if not RUNNING_IN_DOCKER:
        if not os.path.exists('../.env'):
            print('\nFatal error: Failed to load .env')
            print('Please refer to the readme for configuration instructions.\n')
            sys.exit(4)
        load_dotenv('../.env')

        UPLOAD_FOLDER = '../homey/dist/data/icons'

    # if running in docker, .env is passed in via docker-compose.yml

    # verify frontend config exists. actual load is performed in app::readFrontendConfig()
    if not os.path.exists('./config/config.yml') and not os.path.exists('../homey/dist/config/config.yml'):
        print('\nFatal error: Failed to load config.yml')
        print('Please refer to the readme for configuration instructions.\n')
        sys.exit(4)
    
    WEATHER_LAT = os.environ.get('HOMEY_API_WEATHER_LAT', default='')
    WEATHER_LONG = os.environ.get('HOMEY_API_WEATHER_LONG', default='')
    WEATHER_TZ = os.environ.get('TZ', default='America/New_York')
    WEATHER_UNITS = os.environ.get('HOMEY_API_WEATHER_UNITS', default='Standard')
    WEATHER_ENABLED = not (WEATHER_LAT == '' and WEATHER_LONG == '')
    WEATHER_VALID = WEATHER_ENABLED and validateWeather(WEATHER_LAT, WEATHER_LONG)
    
    PORTAINER_URL = os.environ.get('HOMEY_API_PORTAINER_URL', default='')
    PORTAINER_USER = os.environ.get('HOMEY_API_PORTAINER_USER', default='')
    PORTAINER_PASSWORD = os.environ.get('HOMEY_API_PORTAINER_PASSWORD', default='')
    PORTAINER_ENABLED = not PORTAINER_URL == ''
    
    FLOOD_URL = os.environ.get('HOMEY_API_FLOOD_URL', default='')
    FLOOD_USER = os.environ.get('HOMEY_API_FLOOD_USER', default='')
    FLOOD_PASSWORD = os.environ.get('HOMEY_API_FLOOD_PASSWORD', default='')
    FLOOD_ENABLED = not FLOOD_URL == ''
    
    DOCKER_SOCKET = os.environ.get('HOMEY_API_DOCKER_SOCKET', default='/var/run/docker.sock')
    SYSTEM_MONITOR_FILE = './config/local_machine_data.json'
    VALID_ICON_EXTS = {'png', 'jpeg', 'jpg'}

    # fix service checker for local URLs
    os.environ['NO_PROXY'] = '127.0.0.1,localhost,0.0.0.0'

config = Config
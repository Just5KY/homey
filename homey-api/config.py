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
    RUNNING_IN_DOCKER = os.environ.get('HOMEY_API_RUNNING_IN_DOCKER', 'False').lower() == 'true'

    # if running on metal, load .env file from project root
    if not RUNNING_IN_DOCKER:
        if not os.path.exists('../.env'):
            print('\nFatal error: Failed to load .env')
            print('Please refer to the readme for configuration instructions.\n')
            sys.exit(4)
        load_dotenv('../.env')

    # if running in docker, .env is passed in via docker-compose.yml

    # verify frontend config exists. actual load is performed in app::readFrontendConfig()
    if not os.path.exists('./config/config.yml') and not os.path.exists('../homey/dist/config/config.yml'):
        print('\nFatal error: Failed to load config.yml')
        print('Please refer to the readme for configuration instructions.\n')
        sys.exit(4)
 
    NICEHASH_URL = os.environ.get('HOMEY_API_NICEHASH_URL')
    NICEHASH_API_KEY = os.environ.get('HOMEY_API_NICEHASH_API_KEY')
    NICEHASH_SECRET = os.environ.get('HOMEY_API_NICEHASH_SECRET')
    NICEHASH_ORG_ID = os.environ.get('HOMEY_API_NICEHASH_ORG_ID')
    
    WEATHER_LAT = os.environ.get('HOMEY_API_WEATHER_LAT')
    WEATHER_LONG = os.environ.get('HOMEY_API_WEATHER_LONG')
    WEATHER_VALID = validateWeather(WEATHER_LAT, WEATHER_LONG)
    
    DOCKER_USER_ID = os.environ.get('HOMEY_API_DOCKER_USER_ID')
    DOCKER_GROUP_ID = os.environ.get('HOMEY_API_DOCKER_GROUP_ID')
    DOCKER_SOCKET = os.environ.get('HOMEY_API_DOCKER_SOCKET')
    
    PORTAINER_URL = os.environ.get('HOMEY_API_PORTAINER_URL')
    PORTAINER_USER = os.environ.get('HOMEY_API_PORTAINER_USER')
    PORTAINER_PASSWORD = os.environ.get('HOMEY_API_PORTAINER_PASSWORD')
    
    FLOOD_URL = os.environ.get('HOMEY_API_FLOOD_URL')
    FLOOD_USER = os.environ.get('HOMEY_API_FLOOD_USER')
    FLOOD_PASSWORD = os.environ.get('HOMEY_API_FLOOD_PASSWORD')
    
    SYSTEM_MONITOR_FILE = './config/local_machine_data.json'
    VALID_ICON_EXTS = {'png', 'jpeg', 'jpg'}

config = Config
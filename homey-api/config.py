import os
from dotenv import load_dotenv


class Config:
    CONFIG_ERROR = False
    if not os.exists('../.env'):
        print('Error loading .env file. Does it exist in the root directory? Is homey-api being run properly via run.sh/docker?')
        CONFIG_ERROR = True

    load_dotenv('../.env')

    NICEHASH_URL = os.environ.get('HOMEY_API_NICEHASH_URL')
    NICEHASH_API_KEY = os.environ.get('HOMEY_API_NICEHASH_API_KEY')
    NICEHASH_SECRET = os.environ.get('HOMEY_API_NICEHASH_SECRET')
    NICEHASH_ORG_ID = os.environ.get('HOMEY_API_NICEHASH_ORG_ID')
    
    WEATHER_LAT = os.environ.get('HOMEY_API_WEATHER_LAT')
    WEATHER_LONG = os.environ.get('HOMEY_API_WEATHER_LONG')
    
    DOCKER_USER_ID = os.environ.get('HOMEY_API_DOCKER_USER_ID')
    DOCKER_GROUP_ID = os.environ.get('HOMEY_API_DOCKER_GROUP_ID')
    DOCKER_SOCKET = os.environ.get('HOMEY_API_DOCKER_SOCKET')
    
    PORTAINER_URL = os.environ.get('HOMEY_API_PORTAINER_URL')
    PORTAINER_USER = os.environ.get('HOMEY_API_PORTAINER_USER')
    PORTAINER_PASSWORD = os.environ.get('HOMEY_API_PORTAINER_PASSWORD')
    
    FLOOD_URL = os.environ.get('HOMEY_API_FLOOD_URL')
    FLOOD_USER = os.environ.get('HOMEY_API_FLOOD_USER')
    FLOOD_PASSWORD = os.environ.get('HOMEY_API_FLOOD_PASSWORD')
    
    RUNNING_IN_DOCKER = os.environ.get('HOMEY_API_RUNNING_IN_DOCKER')
    DISK_USAGE_FILE = os.environ.get('HOMEY_API_DISK_USAGE_FILE')

config = Config
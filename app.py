from flask import Flask, jsonify
from flask_cors import CORS

from config import config

import nicehash     # miner stats (deprecated)
import open_meteo   # weather
import docker_api   # docker local
import portainer    # docker remote
import flood        # torrents
import local_machine    # disk usage

DEBUG = True

app = Flask(__name__)
app.config.from_object(config)

#nicehash_prod_api = nicehash.private_api(config.NICEHASH_URL, config.NICEHASH_API_KEY, config.NICEHASH_SECRET, config.NICEHASH_ORG_ID)
nicehash_prod_api = None
weather_api = open_meteo.api(config.WEATHER_LAT, config.WEATHER_LONG)
portainer_api = portainer.api(config.PORTAINER_URL, config.PORTAINER_USER, config.PORTAINER_PASSWORD)
docker_api_obj = docker_api.api(config.DOCKER_SOCKET)
flood_api = flood.api(config.FLOOD_URL, config.FLOOD_USER, config.FLOOD_PASSWORD)
local_machine_obj = local_machine.local_machine(config.RUNNING_IN_DOCKER, config.DISK_USAGE_FILE)

CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/nicehashBalances', methods=['GET'])
def nicehashBalances():
    accs = nicehash_prod_api.get_accounts()
    return jsonify(accs)

@app.route('/nicehashMinerStats', methods=['GET'])
def nicehashMinerStats():
    minerStats = nicehash_prod_api.get_mining_algo_stats()
    return jsonify(minerStats)

@app.route('/weatherWeekly', methods=['GET'])
def weatherWeekly():
    return jsonify(weather_api.getWeatherWeekly())

# day format = YYYYMMDD
@app.route('/weatherHourly/<day>', methods=['GET'])
def weatherHourlyDay(day=''):
    return jsonify(weather_api.getWeatherHourly(day))

@app.route('/weatherHourly', methods=['GET'])
def weatherHourly():
    return jsonify(weather_api.getWeatherHourly())

@app.route('/portainerAuth', methods=['GET'])
def portainerAuth():
    return jsonify(portainer_api.authenticate())

@app.route('/portainerList', methods=['GET'])
def portainerList():
    return jsonify(portainer_api.listContainers())

# valid Docker container operations: pause, unpause, start, stop, restart, kill
@app.route('/portainerControl/<containerName>/<operation>', methods=['GET'])
def portainerControl(containerName, operation):
    return jsonify(portainer_api.controlContainer(containerName, operation))

@app.route('/dockerAuth', methods=['GET'])
def dockerAuth():
    return jsonify('True')                  # TODO: implement

@app.route('/dockerList', methods=['GET'])
def dockerList():
    return jsonify(docker_api_obj.listContainers())

# valid Docker container operations: pause, unpause, start, stop, restart, kill
@app.route('/dockerControl/<containerName>/<operation>', methods=['GET'])
def dockerControl(containerName, operation):
    return jsonify(docker_api_obj.controlContainer(containerName, operation))

@app.route('/floodAuth', methods=['GET'])
def floodAuth():
    return jsonify(flood_api.authenticate())

@app.route('/floodStats', methods=['GET'])
def floodStats():
    return jsonify(flood_api.getStats())

@app.route('/floodNotifications', methods=['GET'])
def floodNotifications():
    return jsonify(flood_api.getNotifications())
    
@app.route('/systemInfo', methods=['GET'])
def systemInfo():
    return jsonify(local_machine_obj.getAllInfo());
    
if __name__ == '__main__':
    app.run('0.0.0.0', 9101)

from flask import Flask, jsonify, request
from flask_cors import CORS
import json

from requests.cookies import morsel_to_cookie

import nicehash     # miner stats (deprecated)
import open_meteo   # weather
import portainer    # docker
import flood

from secretKeys import *

#nicehash_prod_api = nicehash.private_api(nicehashHost, orgId, apiKey, apiSecret)
nicehash_prod_api = None
weather_api = open_meteo.api()
portainer_api = portainer.api()
flood_api = flood.api()

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

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
def portainerPause(containerName, operation):
    return jsonify(portainer_api.controlContainer(containerName, operation))

@app.route('/floodAuth', methods=['GET'])
def floodAuth():
    return jsonify(flood_api.authenticate())

@app.route('/floodStats', methods=['GET'])
def floodStats():
    return jsonify(flood_api.getStats())

@app.route('/floodNotifications', methods=['GET'])
def floodNotifications():
    return jsonify(flood_api.getNotifications())
    
if __name__ == '__main__':
    portainer_api.listContainers()
    app.run('0.0.0.0', 9101)

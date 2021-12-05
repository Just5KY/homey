from flask import Flask, jsonify, request
from flask_cors import CORS
import json

from requests.cookies import morsel_to_cookie

import nicehash
import open_meteo   # weather
import portainer
from secretKeys import *

# Not sensitive
weatherHost = 'https://api.open-meteo.com'
#############################################################

nicehash_prod_api = nicehash.private_api(nicehashHost, orgId, apiKey, apiSecret)
weather_api = open_meteo.api(weatherHost)
portainer_api = portainer.api()

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

@app.route('/weatherFull', methods=['GET'])
def weatherFull():
    return jsonify(weather_api.get_all_weather_data())

@app.route('/portainerAuth', methods=['GET'])
def portainerAuth():
    return jsonify(portainer_api.authenticate())

@app.route('/portainerList', methods=['GET'])
def portainerList():
    return jsonify(portainer_api.listContainers())

if __name__ == '__main__':
    portainer_api.listContainers()
    app.run('0.0.0.0', 9101)

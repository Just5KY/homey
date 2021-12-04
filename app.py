from flask import Flask, jsonify, request
from flask_cors import CORS
import json

from requests.cookies import morsel_to_cookie

import nicehash
import open_meteo   # weather
from secretKeys import *

# Not sensitive
weatherHost = 'https://api.open-meteo.com'
#############################################################

nicehash_prod_api = nicehash.private_api(nicehashHost, orgId, apiKey, apiSecret)
weather_api = open_meteo.api(weatherHost)

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

@app.route('/nicehashMinerControl/', methods=['GET', 'POST'])
def nicehashMinerControl():
    print(request.get_json()['action'])
    #actionResp = nicehash_prod_api.send_mining_control_action('stop')
    #return jsonify(actionResp)
    return 'currently_broken' 

@app.route('/weatherFull', methods=['GET'])
def weatherFull():
    return jsonify(weather_api.get_all_weather_data())

if __name__ == '__main__':
    app.run()

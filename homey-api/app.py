from flask import Flask, jsonify, request
from flask_cors import CORS

#import nicehash        # miner stats (deprecated)
from modules import open_meteo       # weather
from modules import docker_api       # docker local
from modules import portainer        # docker remote
from modules import flood            # torrents
from modules import local_machine    # disk usage (work in progress)
from modules import service_checker  # get up/down status of services

from config import config

#print('Portainer validation: ' + str(config.PORTAINER_VALID))

### INITIALIZATION
app = Flask(__name__)
app.config.from_object(config)
CORS(app, resources={r'/*': {'origins': '*'}})

weather_api = open_meteo.api(config.WEATHER_LAT, config.WEATHER_LONG)
portainer_api = portainer.api(config.PORTAINER_URL, config.PORTAINER_USER, config.PORTAINER_PASSWORD)
docker_api_obj = docker_api.api(config.DOCKER_SOCKET)
flood_api = flood.api(config.FLOOD_URL, config.FLOOD_USER, config.FLOOD_PASSWORD)
local_machine_obj = local_machine.local_machine(config.RUNNING_IN_DOCKER, config.DISK_USAGE_FILE)
service_checker_obj = service_checker.service_checker()

nicehash_prod_api = None
#nicehash_prod_api = nicehash.private_api(config.NICEHASH_URL, config.NICEHASH_API_KEY, config.NICEHASH_SECRET, config.NICEHASH_ORG_ID)


### WEATHER
@app.route('/weatherWeekly', methods=['GET'])
def weatherWeekly():
    if not config.WEATHER_VALID:    return jsonify({'Error': 'Weather API not configured'})
    return jsonify(weather_api.getWeatherWeekly())

# day format = YYYYMMDD
@app.route('/weatherHourly/<day>', methods=['GET'])
def weatherHourlyDay(day=''):
    if not config.WEATHER_VALID:    return jsonify({'Error': 'Weather API not configured'})
    return jsonify(weather_api.getWeatherHourly(day))

@app.route('/weatherHourly', methods=['GET'])
def weatherHourly():
    if not config.WEATHER_VALID:    return jsonify({'Error': 'Weather API not configured'})
    return jsonify(weather_api.getWeatherHourly())


### FLOOD
@app.route('/floodAuth', methods=['GET'])
def floodAuth():
    if not flood_api.validConfig:    return jsonify({'Error': 'Flood API not configured'})
    return jsonify(flood_api.authenticate())

@app.route('/floodStats', methods=['GET'])
def floodStats():
    if not flood_api.validConfig:    return jsonify({'Error': 'Flood API not configured'})
    return jsonify(flood_api.getStats())

@app.route('/floodNotifications', methods=['GET'])
def floodNotifications():
    if not flood_api.validConfig:    return jsonify({'Error': 'Flood API not configured'})
    return jsonify(flood_api.getNotifications())


### PORTAINER
@app.route('/portainerAuth', methods=['GET'])
def portainerAuth():
    if not portainer_api.validConfig:    return jsonify({'Error': 'Portainer API not configured'})
    return jsonify(portainer_api.authenticate())

@app.route('/portainerList', methods=['GET'])
def portainerList():
    if not portainer_api.validConfig:    return jsonify({'Error': 'Portainer API not configured'})
    return jsonify(portainer_api.listContainers())

# TODO: rewrite as POST
# valid operations: pause, unpause, start, stop, restart, kill
@app.route('/portainerControl/<containerName>/<operation>', methods=['GET'])
def portainerControl(containerName, operation):
    if not portainer_api.validConfig:    return jsonify({'Error': 'Portainer API not configured'})
    return jsonify(portainer_api.controlContainer(containerName, operation))


### DOCKER
@app.route('/dockerAuth', methods=['GET'])
def dockerAuth():
    return jsonify('True')                  # TODO: implement

@app.route('/dockerList', methods=['GET'])
def dockerList():
    return jsonify(docker_api_obj.listContainers())

# TODO: rewrite as POST
# valid operations: pause, unpause, start, stop, restart, kill
@app.route('/dockerControl/<containerName>/<operation>', methods=['GET'])
def dockerControl(containerName, operation):
    return jsonify(docker_api_obj.controlContainer(containerName, operation))


### LOCAL MACHINE
@app.route('/systemInfo', methods=['GET'])
def systemInfo():
    return jsonify(local_machine_obj.getAllInfo());


### UTILITY
@app.route('/updateServices', methods=['POST'])
def updateServices():
    service_checker_obj.assignAll(request.json)
    service_checker_obj.checkAll()
    return jsonify(request.json)

# @app.route('/addService', methods=['POST'])


### NICEHASH (deprecated)
@app.route('/nicehashBalances', methods=['GET'])
def nicehashBalances():
    accs = nicehash_prod_api.get_accounts()
    return jsonify(accs)

@app.route('/nicehashMinerStats', methods=['GET'])
def nicehashMinerStats():
    minerStats = nicehash_prod_api.get_mining_algo_stats()
    return jsonify(minerStats)


### ENTRYPOINT
if __name__ == '__main__':
    app.run('0.0.0.0', 9101, debug=True)

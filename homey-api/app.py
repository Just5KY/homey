from flask import Flask, jsonify, request
from flask_cors import CORS
import yaml

from config import config
from modules import open_meteo, docker_api, portainer, flood, local_machine, service_checker

#print('Portainer validation: ' + str(config.PORTAINER_VALID))

### INITIALIZATION
app = Flask(__name__)
app.config.from_object(config)
CORS(app, resources={r'/*': {'origins': '*'}})

weatherAPI = open_meteo.api(config.WEATHER_LAT, config.WEATHER_LONG)
portainerAPI = portainer.api(config.PORTAINER_URL, config.PORTAINER_USER, config.PORTAINER_PASSWORD)
dockerAPI = docker_api.api(config.DOCKER_SOCKET)
floodAPI = flood.api(config.FLOOD_URL, config.FLOOD_USER, config.FLOOD_PASSWORD)
localMachine = local_machine.local_machine(config.RUNNING_IN_DOCKER, config.DISK_USAGE_FILE)
serviceChecker = service_checker.service_checker()

### WEATHER
@app.route('/weatherWeekly', methods=['GET'])
def weatherWeekly():
    if not config.WEATHER_VALID:    return jsonify({'Error': 'Weather API not configured'})
    return jsonify(weatherAPI.getWeatherWeekly())

# day format = YYYYMMDD
@app.route('/weatherHourly/<day>', methods=['GET'])
def weatherHourlyDay(day=''):
    if not config.WEATHER_VALID:    return jsonify({'Error': 'Weather API not configured'})
    return jsonify(weatherAPI.getWeatherHourly(day))

@app.route('/weatherHourly', methods=['GET'])
def weatherHourly():
    if not config.WEATHER_VALID:    return jsonify({'Error': 'Weather API not configured'})
    return jsonify(weatherAPI.getWeatherHourly())


### FLOOD
@app.route('/floodAuth', methods=['GET'])
def floodAuth():
    if not floodAPI.validConfig:    return jsonify({'Error': 'Flood API not configured'})
    return jsonify(floodAPI.authenticate())

@app.route('/floodStats', methods=['GET'])
def floodStats():
    if not floodAPI.validConfig:    return jsonify({'Error': 'Flood API not configured'})
    return jsonify(floodAPI.getStats())

@app.route('/floodNotifications', methods=['GET'])
def floodNotifications():
    if not floodAPI.validConfig:    return jsonify({'Error': 'Flood API not configured'})
    return jsonify(floodAPI.getNotifications())


### PORTAINER
@app.route('/portainerAuth', methods=['GET'])
def portainerAuth():
    if not portainerAPI.validConfig:    return jsonify({'Error': 'Portainer API not configured'})
    return jsonify(portainerAPI.authenticate())

@app.route('/portainerList', methods=['GET'])
def portainerList():
    if not portainerAPI.validConfig:    return jsonify({'Error': 'Portainer API not configured'})
    return jsonify(portainerAPI.listContainers())

# TODO: rewrite as POST
# valid operations: pause, unpause, start, stop, restart, kill
@app.route('/portainerControl/<containerName>/<operation>', methods=['GET'])
def portainerControl(containerName, operation):
    if not portainerAPI.validConfig:    return jsonify({'Error': 'Portainer API not configured'})
    return jsonify(portainerAPI.controlContainer(containerName, operation))


### DOCKER
@app.route('/dockerAuth', methods=['GET'])
def dockerAuth():
    return jsonify('True')                  # TODO: implement

@app.route('/dockerList', methods=['GET'])
def dockerList():
    return jsonify(dockerAPI.listContainers())

# TODO: rewrite as POST
# valid operations: pause, unpause, start, stop, restart, kill
@app.route('/dockerControl/<containerName>/<operation>', methods=['GET'])
def dockerControl(containerName, operation):
    return jsonify(dockerAPI.controlContainer(containerName, operation))


### LOCAL MACHINE
@app.route('/systemInfo', methods=['GET'])
def systemInfo():
    return jsonify(localMachine.getAllInfo());


### SERVICE CHECKER
@app.route('/updateServices', methods=['POST'])
def updateServices():
    serviceChecker.assignAll(request.json)
    return jsonify(serviceChecker.checkAll())

# @app.route('/addService', methods=['POST'])


### SETTINGS
@app.route('/writeFrontendConfig', methods=['POST'])
def writeFrontendConfig():
    try:
        with open('../homey/src/assets/config.yml', 'w') as f:
            yaml.dump(request.json, f)
    except: 
        return jsonify({'Error': 'Could not write new config file. Are permissions correct?'})

    return jsonify({'Success': 'Wrote updated config file'})


### NICEHASH (deprecated)
nicehash_prodAPI = None
@app.route('/nicehashBalances', methods=['GET'])
def nicehashBalances():
    accs = nicehash_prodAPI.get_accounts()
    return jsonify(accs)

@app.route('/nicehashMinerStats', methods=['GET'])
def nicehashMinerStats():
    minerStats = nicehash_prodAPI.get_mining_algo_stats()
    return jsonify(minerStats)


### ENTRYPOINT
if __name__ == '__main__':
    app.run('0.0.0.0', 9101, debug=True)

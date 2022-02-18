from genericpath import exists
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import yaml

from config import config
from modules import open_meteo, docker_api, portainer, flood, service_checker

### INITIALIZATION
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

app.config.from_object(config)
app.config['JSON_SORT_KEYS'] = False

if config.RUNNING_IN_DOCKER == True:
    app.config['UPLOAD_FOLDER'] = './config/icons'  
else:
    app.config['UPLOAD_FOLDER'] = '../homey/dist/data/icons'

weatherAPI = open_meteo.api(config.WEATHER_LAT, config.WEATHER_LONG)
portainerAPI = portainer.api(config.PORTAINER_URL, config.PORTAINER_USER, config.PORTAINER_PASSWORD)
dockerAPI = docker_api.api(config.DOCKER_SOCKET)
floodAPI = flood.api(config.FLOOD_URL, config.FLOOD_USER, config.FLOOD_PASSWORD)
serviceChecker = service_checker.service_checker()

def readConfigFile():
    with open('./config/config.yml') as f:
        cfg = jsonify(yaml.safe_load(f))
        serviceChecker.assignAll(cfg.json['services'])
        return cfg

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
    if not config.FLOOD_ENABLED:    return jsonify({'Error': 'Flood API not configured'})
    return jsonify(floodAPI.authenticate())

@app.route('/floodStats', methods=['GET'])
def floodStats():
    if not config.FLOOD_ENABLED:    return jsonify({'Error': 'Flood API not configured'})
    return jsonify(floodAPI.getStats())

@app.route('/floodNotifications', methods=['GET'])
def floodNotifications():
    if not config.FLOOD_ENABLED:    return jsonify({'Error': 'Flood API not configured'})
    return jsonify(floodAPI.getNotifications())


### PORTAINER
@app.route('/portainerAuth', methods=['GET'])
def portainerAuth():
    if not config.PORTAINER_ENABLED:    return jsonify({'Error': 'Portainer API not configured'})
    return jsonify(portainerAPI.authenticate())

@app.route('/portainerList', methods=['GET'])
def portainerList():
    if not config.PORTAINER_ENABLED:    return jsonify({'Error': 'Portainer API not configured'})
    return jsonify(portainerAPI.listContainers())

@app.route('/portainerControl', methods=['POST'])
def portainerControl():
    if not config.PORTAINER_ENABLED:    return jsonify({'Error': 'Portainer API not configured'})
    return jsonify(portainerAPI.controlContainer(request.json['name'], request.json['operation']))

### DOCKER
@app.route('/dockerList', methods=['GET'])
def dockerList():
    return jsonify(dockerAPI.listContainers())

@app.route('/dockerControl', methods=['POST'])
def dockerControl():
    return jsonify(dockerAPI.controlContainer(request.json['name'], request.json['operation']))


### LOCAL MACHINE
@app.route('/systemInfo', methods=['GET'])
def systemInfo():
    if not exists(config.SYSTEM_MONITOR_FILE):
        return jsonify({'Error': config.SYSTEM_MONITOR_FILE + ' does not exist'})

    with open(config.SYSTEM_MONITOR_FILE, 'r') as f:
        return Response(f.read(), mimetype="text/json");        

### SERVICE CHECKER
@app.route('/checkServices', methods=['GET'])
def checkServices():
    if serviceChecker.services == []:
        readConfigFile()
    return jsonify(serviceChecker.checkAll())

@app.route('/ping', methods=['GET'])
def ping():
    return {'status': 'up'}

### SETTINGS
@app.route('/writeFrontendConfig', methods=['POST'])
def writeFrontendConfig():
    try:
        with open('./config/config.yml', 'w') as f:
            yaml.dump(request.json, f, sort_keys=False)
    except: 
        return jsonify({'Error': 'Could not write new config file. Are permissions correct?'})

    serviceChecker.assignAll(request.json['services'])
    return jsonify({'Success': 'Wrote updated config file'})

@app.route('/readFrontendConfig', methods=['GET'])
def readFrontendConfig():
    try:
        return readConfigFile()
    except: 
        return jsonify({'Error': 'Could not read config file. Are permissions correct?'})

@app.route('/uploadIcon', methods=['POST'])
def uploadIcon():
    try:
        f = request.files['image']
        if f and f.filename != '' and '.' in f.filename and f.filename.rsplit('.')[1].lower() in config.VALID_ICON_EXTS:
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify ({'Success': 'Uploaded ' + f.filename})
    except:
        print('Error saving to ' + app.config['UPLOAD_FOLDER'] + '. Are permissions correct?')
    return jsonify({'Error': 'Could not upload image. Check logs for details.'})

@app.route('/getIconPath/<filename>', methods=['GET'])
def getIcon(filename):
    paths = os.listdir(app.config['UPLOAD_FOLDER'])
    if filename == 'all':   return jsonify(paths)
    if exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        return jsonify(filename)
    return jsonify({'Error': 'Image not found: ' + os.path.join(app.config['UPLOAD_FOLDER'], filename)})


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


from genericpath import exists
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import yaml
import copy
import threading

from config import config
from modules import service_checker, open_meteo, docker_api, portainer, flood

### INITIALIZATION
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

app.config.from_object(config)
app.config['JSON_SORT_KEYS'] = False

if config.WEATHER_VALID:        weatherAPI = open_meteo.api(config.WEATHER_LAT, config.WEATHER_LONG)
if config.PORTAINER_ENABLED:    portainerAPI = portainer.api(config.PORTAINER_URL, config.PORTAINER_USER, config.PORTAINER_PASSWORD)
if config.FLOOD_ENABLED:        floodAPI = flood.api(config.FLOOD_URL, config.FLOOD_USER, config.FLOOD_PASSWORD)
dockerAPI = docker_api.api(config.DOCKER_SOCKET)
serviceChecker = service_checker.service_checker()

def readConfigFile():
    with open('./config/config.yml') as f:
        cfg = jsonify(yaml.safe_load(f))
        serviceChecker.assignAll(cfg.json['services'])

        # strip ?=new from image names in config file (appended on upload to cache bust)
        retCfg = copy.deepcopy(cfg)
        cfg.set_data(cfg.get_data(as_text=True).replace('?=new', ''))

    # write stripped image names
    with open('./config/config.yml', 'w+') as f:
        yaml.dump(cfg.json, f, sort_keys=False)

    return retCfg

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
    # if not config.FLOOD_ENABLED:    return jsonify({'Error': 'Flood API not configured'})
    # return jsonify(floodAPI.getNotifications())

    # FAKE DEMO DATA

    return jsonify([
        {
            "msg": "Animal Collective - Time Skiffs (2022) [FLAC]",
            "time": "02/20 12:29 AM"
        },
        {
            "msg": "Ecco2K - Amygdala (2022) [FLAC]",
            "time": "02/18 1:49 AM"
        },
        {
            "msg": "Steve Roach - Structures From Silence (1984) [FLAC]",
            "time": "02/11 3:42 AM"
        },
        {
            "msg": "debian-11.2.0-amd64-DVD-1.iso",
            "time": "02/09 8:51 PM"
        },
        {
            "msg": "The.Longest.Yard.1974.720p.Blueray.x264-x0r",
            "time": "02/17 2:01 PM"
        },
        {
            "msg": "The Animatrix (2003) 1080p BrRip x264 - YIFY",
            "time": "02/17 1:59 PM"
        },
        {
            "msg": "Secret Circle - Tube Socks (2017) [Single]",
            "time": "02/19 4:19 AM"
        },
        {
            "msg": "How.To.With.John.Wilson.S01.1080p.AMZN.WEBRip.DDP5.1.x264-NTb",
            "time": "02/17 1:18 PM"
        },
        {
            "msg": "Paprika 2006 JAPANESE 1080p BluRay H264 AAC-VXT",
            "time": "02/14 1:59 PM"
        },
        {
            "msg": "Higher Brothers - Black Cab [WEB FLAC]",
            "time": "02/14 1:54 PM"
        },
        {
            "msg": "Datach'i - System (Bonus Tracks) (2016)",
            "time": "02/14 1:53 PM"
        },
        {
            "msg": "Ski Mask the Slump God - Beware the Book of Eli (2018) [WEB - FLAC]",
            "time": "02/11 8:16 PM"
        },
        {
            "msg": "Code Monkeys - Seasons 1-2 + Extras (Complete)",
            "time": "02/11 3:52 AM"
        },
        {
            "msg": "Firefly.2002.S01.1080p.x265.HEVC",
            "time": "02/09 8:40 PM"
        },
        {
            "msg": "Seinfeld (1989) S01-S09 (Mixed)",
            "time": "02/09 8:39 PM"
        },
        {
            "msg": "bladee - The Fool (2021) [WEB-FLAC]",
            "time": "02/09 8:28 PM"
        },
        {
            "msg": "Subtronics - FRACTALS (2022) [WEB-FLAC]",
            "time": "02/09 8:27 PM"
        },
        {
            "msg": "Adobe.Master.Collection.CC.2022.x64.Multilingual",
            "time": "02/18 1:38 AM"
        }
    ])


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

    serviceChecker.checkAll()
        
    return jsonify(serviceChecker.getStatuses())

@app.route('/updateService', methods=['POST'])
def updateService():
    if serviceChecker.services == []:
        readConfigFile()
    if serviceChecker.updateServiceURL(request.json):
        return {'success': 'updated service'}
    return {'error': 'failed to update service'}

@app.route('/addService', methods=['POST'])
def addService():
    serviceChecker.addService(request.json)
    return {'success': 'added new service'}

@app.route('/deleteService', methods=['POST'])
def deleteService():
    if serviceChecker.deleteService(request.json):
        return {'success': 'deleted service'}
    return {'error': 'failed to delete service'}

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
        print(f.filename.rsplit('.', 1), flush=True)
        if f and f.filename != '' and f.filename.rsplit('.', 1)[1] in config.VALID_ICON_EXTS:
            f.save(os.path.join(config.UPLOAD_FOLDER, secure_filename(f.filename)))
            return jsonify ({'Success': 'Uploaded ' + f.filename})
    except:
        print('Error saving to ' + config.UPLOAD_FOLDER + '. Are permissions correct?')
    return jsonify({'Error': 'Could not upload image. Check logs for details.'})

@app.route('/getIconPath/<filename>', methods=['GET'])
def getIcon(filename):
    paths = os.listdir(config.UPLOAD_FOLDER)
    if filename == 'all':   return jsonify(paths)
    if exists(os.path.join(config.UPLOAD_FOLDER, filename)):
        return jsonify(filename)
    return jsonify({'Error': 'Image not found: ' + os.path.join(config.UPLOAD_FOLDER, filename)})


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
    # debug script serves /public, not /dist
    config.UPLOAD_FOLDER = '../homey/public/data/icons'

    if config.RUNNING_IN_DOCKER:
        print('Warning: RUNNING_IN_DOCKER is set to True, but the debug server is running. Should it be set to False?')
        
    app.run('0.0.0.0', 9101, debug=True)

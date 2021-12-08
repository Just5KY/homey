# // POST /api/auth/authenticate
#{
#   username: floodUser,
#   password: floodPassword,
# }

import requests
import json
from datetime import datetime
from dateutil.parser import parse
from secretKeys import floodURL, floodUser, floodPassword

class api:

    def __init__(self):
        self.host = floodURL
        self.user = {
            "username": floodUser,
            "password": floodPassword
        }
        self.session = None
    
    def authenticate(self):
        ses = requests.Session()

        userData = self.user
        response = ses.request('POST', url=self.host + '/auth/authenticate', data=userData)

        try:
            self.session = ses
            return response.json()['success']
        except:
            self.session = None
            return False

    def getStats(self):
        if self.session == None:
            self.authenticate()

        # get 5 minutes of up/down stats (delta 6s)
        minuteDataRaw = self.session.request('GET', self.host + '/history', params={'snapshot': 'FIVE_MINUTE'})
        # get 24 hours of up/down stats (delta 1hr)
        dailyDataRaw = self.session.request('GET', self.host + '/history', params={'snapshot': 'DAY'})
        
        i = 0
        totalDownload = 0.0
        totalUpload = 0.0
        for t in dailyDataRaw.json()['timestamps']:
            timeChunk = datetime.fromtimestamp(dailyDataRaw.json()['timestamps'][i]/1000)
            totalDownload += dailyDataRaw.json()['download'][i]
            totalUpload += dailyDataRaw.json()['upload'][i]
            i += 1

        avgUp = 0
        avgDown = 0
        for j in range(0, 5):   # Average up/down speed based on the last 5 frames (30 seconds) of data
            avgDown += dailyDataRaw.json()['download'][j]
            avgUp += dailyDataRaw.json()['upload'][j]

        returnData = {
            'dailyDownloaded': formatBytes(totalDownload*1000),
            'dailyUploaded': formatBytes(totalUpload*1000),
            'downSpeed': formatBytes(avgDown / 5) + '/s',
            'upSpeed': formatBytes(avgUp / 5) + '/s',
        }
 
        return returnData

    def getNotifications(self):
        if self.session == None:
            self.authenticate()

        response = self.session.request('GET', url=self.host + '/notifications')

        returnData = []
        for n in response.json()['notifications']:
            if n['id'] != 'notification.torrent.finished':  # only get notifications for finished torrents
                continue
            returnData.append({
                'msg': n['data']['name'],
                'time': datetime.fromtimestamp(n['ts']/1000)
            })
        
        return returnData

def formatBytes(size):
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'k', 2: 'm', 3: 'g', 4: 't'}
    while size > power:
        size /= power
        n += 1
    return str(int(round(size))) + power_labels[n]+'b'

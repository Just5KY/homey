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

        # calculate total uploaded/downloaded amount for the last 24 hours
        totalDownload = 0.0
        totalUpload = 0.0
        for i, t in enumerate(dailyDataRaw.json()['timestamps']):
            #timeChunk = datetime.fromtimestamp(t/1000)
            downHour = dailyDataRaw.json()['download'][i]
            upHour = dailyDataRaw.json()['upload'][i]

            if downHour is not None:
                totalDownload += downHour
            if upHour is not None:
                totalUpload += upHour

        # calculate current upload/download speed and format data for speed chart
        avgUp = 0
        avgDown = 0
        minuteData = []
        for i, m in enumerate(minuteDataRaw.json()['timestamps']):
            # Average up/down speed based on the last 3 frames (18 seconds) of data
            if i > len(minuteDataRaw.json()['timestamps']) - 4: 
                avgDown += minuteDataRaw.json()['download'][i]
                avgUp += minuteDataRaw.json()['upload'][i]
            # Return each 6-second frame over the last 5 minutes
            minuteData.append({
                'time': datetime.fromtimestamp(m/1000).strftime('%-I:%M:%S'),
                'down': minuteDataRaw.json()['download'][i],    #formatBytes(minuteDataRaw.json()['download'][i]),
                'up': minuteDataRaw.json()['upload'][i]         #formatBytes(minuteDataRaw.json()['upload'][i])
            })

        return {
            'dailyDownloaded': formatBytes(totalDownload*1000),
            'dailyUploaded': formatBytes(totalUpload*1000),
            'downSpeed': formatBytes(avgDown / 3) + '/s',
            'upSpeed': formatBytes(avgUp / 3) + '/s',
            'minuteData': minuteData
        }

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
                'time': datetime.fromtimestamp(n['ts']/1000).strftime("%m/%d %-I:%M %p")
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

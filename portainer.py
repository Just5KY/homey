import requests
import json
from secretKeys import portainerURL, portainerUser, portainerPassword

class api:

    def __init__(self):
        self.host = portainerURL
        self.user = {
            "Username": portainerUser, 
            "Password": portainerPassword
        }
        self.authToken = ''
        self.endpointId = ''

    def authenticate(self):
        ses = requests.Session()

        userData = json.dumps(self.user)
        response = ses.request('POST', url=self.host + '/auth', data=userData)

        if response.status_code != 200:
            raise Exception(str(response.status_code) + ": " + response.reason)
            
        # Set authentication token
        self.authToken = 'Bearer ' + response.json()['jwt']

        # Get endpoint id for all subsequent calls
        rawEndpoint = ses.request('GET', url=self.host + '/endpoints', 
            headers={"Authorization": self.authToken}
        )
        self.endpointId = rawEndpoint.json()[0]['Id']

        return True
            

    def listContainers(self):
        ses = requests.Session()

        # If not authenticated yet, do so
        if self.authToken == '':
            self.authenticate()

        response = ses.request('GET', 
            url=self.host + '/endpoints/' + str(self.endpointId) + '/docker/containers/json', 
            headers={"Authorization": self.authToken},
            data=json.dumps({'all': True})
        )

        if response.status_code != 200:
            raise Exception(str(response.status_code) + ": " + response.reason)
        
        containerData = []
        for con in response.json():
            newCon = {}
            newCon['name'] = con['Names'][0][1:]
            newCon['status'] = con['State']
            newCon['uptime'] = con['Status'].lower().replace(' (healthy)', '')
            containerData.append(newCon)

        return {'containers': containerData}
            
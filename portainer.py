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

    def authenticate(self):
        ses = requests.Session()
        
        userData = json.dumps(self.user)
        response = ses.request('POST', url=self.host + '/auth', data=userData)

        if response.status_code == 200:
            # Set authentication token
            self.authToken = response.json()['jwt']

            # Get endpoint id for all subsequent calls
            rawEndpoint = ses.request('GET', 
                url=self.host + '/endpoints', 
                headers={"Authorization": "Bearer " + self.authToken}
            )
            self.endpointId = rawEndpoint.json()[0]['Id']

            return True
        else:
            raise Exception(str(response.status_code) + ": " + response.reason)

    def listContainers(self):
        ses = requests.Session()
        if self.authToken == '':
            self.authenticate()

        

        response = ses.request('GET', 
            url=self.host + '/endpoints/2/docker/containers/json', 
            headers={"Authorization": "Bearer " + self.authToken},
            data=json.dumps("all==true")
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(str(response.status_code) + ": " + response.reason)
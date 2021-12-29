from urllib import response
import requests
import json

class api:

    def __init__(self, portainerURL, portainerUser, portainerPassword):
        self.host = portainerURL
        self.user = {
            "Username": portainerUser, 
            "Password": portainerPassword
        }
        self.authToken = ''
        self.endpointId = ''
        self.validConfig = self.authenticate()

    def authenticate(self):
        ses = requests.Session()
        userData = json.dumps(self.user)

        try:
            response = ses.request('POST', url=self.host + '/auth', data=userData, timeout=5)
        except:
            print('Error: Could not connect to Portainer API at ' + self.host)
            return False

        if response.status_code != 200:
            print('Error: Bad Portainer credentials')
            return False
            
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
            params={'all': 'true'}  # without this only running containers are returned
        )

        if response.status_code != 200:
            raise Exception(str(response.status_code) + ": " + response.reason)
        
        containerData = []
        for con in response.json():
            containerData.append({
                'id': con['Id'],
                'name': con['Names'][0].replace('/', ''),
                'status': con['State'],
                'uptime': con['Status']
            })

        return containerData
            
    # valid operations: pause, unpause, start, stop, restart, kill
    def controlContainer(self, containerName, operation):
        ses = requests.Session()
        # If not authenticated yet, do so
        if self.authToken == '':
            self.authenticate()

        targetId = ''
        for con in self.listContainers():
            if con['name'] == containerName.lower():
                targetId = con['id']
                break

        if targetId == '':
            return 'error: ' + containerName + ' not found'

        response = ses.request('POST', 
            url=self.host + '/endpoints/' + str(self.endpointId) + '/docker/containers/' + targetId + '/' + operation, 
            headers={"Authorization": self.authToken}
        )

        if response.status_code == 204:
            return 'success'

        return response.json()  # Error information
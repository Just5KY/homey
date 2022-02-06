import docker
from urllib import response
import requests
import json
from datetime import datetime
import time

class api:

    def __init__(self, dockerSocketPath):
        if dockerSocketPath == '/var/run/docker.sock':   # default
            self.client = docker.from_env()
            self.api_client = docker.APIClient(base_url='unix:/' + dockerSocketPath)
        else:
            print('ERROR: Custom docker socket paths are not yet supported.')

    def listContainers(self):
        containerData = []
        
        for c in self.client.api.containers(all=True):
            containerData.append({
                'id': c['Id'],
                'name': c['Names'][0].replace('/', ''),
                'status': c['State'],
                'uptime': c['Status']
            })

        return containerData

    # valid operations: pause, unpause, start, stop, restart, kill, info
    def controlContainer(self, containerName, operation):     
        targetId = ''
        for con in self.listContainers():
            if con['name'] == containerName.lower():
                targetId = con['id']
                break

        if targetId == '':
            return 'error: ' + containerName + ' not found'

        container = self.client.containers.get(targetId)
        
        # get detailed container stats & logs
        if operation == 'info':
            stats = self.api_client.inspect_container(targetId)
            logs = []

            rawLogs = self.api_client.logs(targetId, timestamps=True, tail=100).split(b'\n')
            for line in rawLogs:
                logs.append(line.decode().replace('\"','').strip())
            logs.pop()  # trim blank line

            return { 'stats': stats, 'log': logs }

        # every other operation name is a valid Docker API method
        try:
            targetOp = getattr(container, operation)
            targetOp()
        except:
            return 'error: could not ' + operation + ' ' + containerName

        return 'success'
        


        
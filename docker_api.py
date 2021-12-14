import docker
from urllib import response
import requests
import json
from datetime import datetime
import time
from secretKeys import dockerSocketPath

class api:

    def __init__(self):
        if dockerSocketPath == '/var/run/docker.sock':   # default
            self.client = docker.from_env()
        else:
            print('unhandled')

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

    # valid operations: pause, unpause, start, stop, restart, kill
    def controlContainer(self, containerName, operation):     
        targetId = ''
        for con in self.listContainers():
            if con['name'] == containerName.lower():
                targetId = con['id']
                break

        if targetId == '':
            return 'error: ' + containerName + ' not found'

        try:
            container = self.client.containers.get(targetId)
            targetOp = getattr(container, operation)
            targetOp()
        except:
            return 'error: could not ' + operation + ' ' + containerName

        return 'success'
        


        
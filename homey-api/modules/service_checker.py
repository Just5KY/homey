import requests
from requests_futures.sessions import FuturesSession
from urllib3.exceptions import InsecureRequestWarning

class service_checker:
    services = []
    statuses = []
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

    def assignAll(self, services):
        self.services = services
        self.session = requests.Session()

    def addService(self, service):
        self.services.append(service)

    def deleteService(self, service):
        for s in self.services:
            if s['name'] == service['name']:
                self.services.remove(service)
                return True
        return False

    def updateServiceURL(self, service):
        for s in self.services:
            if s['name'] == service['name']:
                s['url'] = service['url']
                return True
        return False

    def getStatuses(self):
        return self.statuses

    def checkAll(self):
        newStatuses = []
        # for s in self.services:
        #     newStatuses.append({
        #         'name': s['name'],
        #         'up': self.checkService(s)
        #     })
        # self.statuses = newStatuses
        with FuturesSession(max_workers=len(self.services)) as ses:
            for s in self.services:
                up = False
                future = ses.get(s['url'], verify=False, timeout=1.5)
                try:
                    up = future.result().status_code < 404
                except:
                    up = False

                newStatuses.append({
                    'name': s['name'],
                    'up': up
                })
        self.statuses = newStatuses
        return newStatuses

    # returns true if the URL is reachable
    def checkService(self, service):
        try:
            res = self.session.get(service['url'], verify=False, timeout=1.5)
        except:
            return False

        return (res.status_code < 404)

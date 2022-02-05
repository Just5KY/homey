import requests
from urllib3.exceptions import InsecureRequestWarning

class service_checker:
    services = []
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

    def assignAll(self, services):
        self.services = services

    def addService(self, service):
        self.services.append(service)

    def checkAll(self):
        statuses = []
        for s in self.services:
            statuses.append({
                'name': s['name'],
                'up': self.checkService(s['url'])
            })
        return statuses

    # returns true if the URL is reachable
    def checkService(self, url):
        try:
            res = requests.get(url, verify=False, timeout=5)
        except:
            return False

        return (res.status_code < 404)

from genericpath import exists
from shutil import disk_usage
import psutil

# todo: move docker file reading to another class
# too messy to put ifs in every method

class local_machine:
    def __init__(self, runningInDocker, diskUsageFile):
        self.diskUsageFile = diskUsageFile      # file determines which paths/drives to report on
        self.runningInDocker = runningInDocker
        self.procHandle = psutil.Process()

    def getAllInfo(self):
        return({
            'diskUsage': self.getDiskUsage(),
            'cpuPercent': self.getCPU(),
            'ramUsage': self.getRAM()
        })

    def getDiskUsage(self):
        if self.diskUsageFile == '':
            return 'Error: Disk usage disabled in config'

        if not exists(self.diskUsageFile):
            return 'Error: Disk config file not found: ' + self.diskUsageFile

        with open(self.diskUsageFile, 'r') as f:
            diskUsage = []
            for d in f.readlines():
                if d.split() == []: continue
                
                if self.runningInDocker: 
                    diskUsage.append(self.diskLineToJSON(d))
                else:
                    d = d[:d.find(':')].replace('root', '/')
                    total, used, free = disk_usage(d)
                    diskUsage.append(
                        self.diskLineToJSON(
                            d + ' ' + str(total // (2**30)) + ' ' + 
                            str(used // (2**30)) + ' ' + str(free // (2**30)
                        ))
                    )
            return diskUsage

    def getCPU(self):
        return self.procHandle.cpu_percent()

    # return values formatted in megabytes
    def getRAM(self):
        raw = psutil.virtual_memory()

        return {
            'total': round(psutil.virtual_memory()[0] / 1000000),
            'free':  round(psutil.virtual_memory()[1] / 1000000),
            'used': round(psutil.virtual_memory()[3] / 1000000),
            'percent_used': psutil.virtual_memory()[2]
        }

    def diskLineToJSON(self, line):
        arr = line.split()
        return {
            'disk':  arr[0].replace(':', ''),
            'total': int(arr[1]),
            'used':  int(arr[2]),
            'free':  int(arr[3]),
            'percent_used': round(int(arr[2]) / int(arr[1]) * 100)
            }
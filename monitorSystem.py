from genericpath import exists
from shutil import disk_usage
import psutil
import time

# run on host
# reads disk/CPU/RAM usage and writes to file

# CONFIGURATION #########################################################

# If running in Docker, dataFile must be accessible inside the container
dataFile = './homey-api/local_machine_data.txt'     # file to write to
watchedDisks = ['/']                                # list of disks to report on: '/', '/mnt/media', etc
intervalMinutes = 1                                 # write to file every X minutes
intervalCPUCalc = 6                                 # average CPU usage over X seconds  

#########################################################################

# get free, available, & total space for each disk in watchedDisks
def getDiskUsage():
    if len(watchedDisks) < 1:   return
    if not exists(dataFile):    return 'Error: Data file not found ' + dataFile

    diskUsage = []
    for d in watchedDisks:
        if d.split() == []: continue
        
        total, used, free = disk_usage(d)
        diskUsage.append(formatDiskLine(d, total, used, free))
    return diskUsage

# average CPU usage over specified seconds (blocking)
def getCPUUsage():
    return str(psutil.cpu_percent(intervalCPUCalc)) + '\n'

# return values formatted in megabytes as JSON string
def getRAMUsage():
    raw = psutil.virtual_memory()

    return str({
        'total': round(psutil.virtual_memory()[0] / 1000000),
        'free':  round(psutil.virtual_memory()[1] / 1000000),
        'used': round(psutil.virtual_memory()[3] / 1000000),
        'percent_used': psutil.virtual_memory()[2]
    }) + '\n'

# convert int disk usage values to JSON string
def formatDiskLine(label, total, free, used):
    disk = (label + ' ' + str(total // (2**30)) + ' ' + str(used // (2**30)) + ' ' + str(free // (2**30))).split()

    return str({
        'disk':  disk[0].replace(':', ''),
        'total': int(disk[1]),
        'used':  int(disk[2]),
        'free':  int(disk[3]),
        'percent_used': round(int(disk[2]) / int(disk[1]) * 100)
    }) + '\n'

# entrypoint
while(True):
    currentCPU = getCPUUsage()  # blocks for 6 seconds

    with open(dataFile, 'w') as f:
        f.writelines(getDiskUsage())
        f.writelines([currentCPU, getRAMUsage()])

    time.sleep( (intervalMinutes * 60) - intervalCPUCalc)

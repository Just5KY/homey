from genericpath import exists
from shutil import disk_usage
from psutil import cpu_percent, virtual_memory
from time import sleep
import json

# Run on host (outside of Docker)
# If homey is running in Docker, dataFile must be accessible inside the container

# Gets disk/CPU/RAM usage and writes JSON to file

# CONFIGURATION #########################################################

dataFile = "./homey-api/local_machine_data.json"    # file to write to
watchedDisks = ["/"]                                # list of disks to report on: "/", "/mnt/media", etc
intervalMinutes = 2                                 # write to file every X minutes
intervalCPUCalc = 6                                 # average CPU usage over X seconds  

#########################################################################

# get free, available, & total space for each disk in watchedDisks
def getDiskUsage():
    if len(watchedDisks) < 1:   return
    if not exists(dataFile):    return "Error: Data file not found " + dataFile

    diskUsage = []
    for d in watchedDisks:
        if d.split() == []: continue
        
        total, used, free = disk_usage(d)
        diskUsage.append(formatDiskLine(d, total, used, free))
    return '\"disks\": [ ' + ', '.join(diskUsage) + ' ]'

# average CPU usage over intervalCPUCalc seconds
# blocks for intervalCPUCalc seconds
def getCPUUsage():
    return '\"cpu\": ' + str(cpu_percent(intervalCPUCalc))

# return values formatted in megabytes as JSON string
def getRAMUsage():
    raw = virtual_memory()

    return '\"ram\": ' + json.dumps({
        "total": round(raw[0] / 1000000),
        "free":  round(raw[1] / 1000000),
        "used": round(raw[3] / 1000000),
        "percent_used": raw[2]
    })

# convert int disk usage values to JSON string
def formatDiskLine(label, total, used, free):
    return json.dumps({
        "label":  label.replace(":", ""),
        "total": total // (2**30),
        "used":  used // (2**30),
        "free":  free // (2**30),
        "percent_used": round((used / total) * 100)
    })

# entrypoint
while(True):
    currentCPU = getCPUUsage()  # blocks for intervalCPUCalc seconds

    with open(dataFile, "w") as f:
        f.write('{ ')
        f.write(getDiskUsage() + ', ')
        f.write(currentCPU + ', ')
        f.write(getRAMUsage())
        f.write(' }')

    sleep( (intervalMinutes * 60) - intervalCPUCalc)

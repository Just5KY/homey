from genericpath import exists
from shutil import disk_usage
from psutil import cpu_percent, virtual_memory, boot_time
from time import sleep, time
from datetime import datetime, timedelta
from socket import gethostname
import json


# README ################################################################
# Writes CPU, RAM, and disk usage to a .json file for Docker containers.
#
# 0. pip install psutil
# 1. Configure dataFile to match homey-api's /config volume mount point.
# 2. Configure watchedDisks if desired.
# 3. Run on host machine (where docker engine is running). 
#
# This script will write to the file every intervalSeconds.
# Homey-api will read it intermittently to display performance stas.
# CONFIGURATION #########################################################
dataFile = "./homey-api/local_machine_data.json"    # output file
watchedDisks = ["/"]    # report disk usage for: "/", "/mnt/media", etc
intervalSeconds = 30    # write to file every X seconds
intervalCPUCalc = 6     # average CPU usage over X seconds  
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

# get system uptime
def getUptime():
    secondsUp = time() - boot_time()
    uptime = datetime(1,1,1) + timedelta(seconds=secondsUp)
    toReturn = '\"uptime\": \"'

    if uptime.day-1 > 0:
        toReturn += ('%d days, ' % uptime.day-1)
    if uptime.hour > 0:
        toReturn += ('%d hours, ' % uptime.hour)
    toReturn += ('%d minutes\"' % uptime.minute)

    return toReturn

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
        f.write('\"hostname\" : \"' + gethostname() + '\", ')
        f.write(getUptime() + ', ')
        f.write(getDiskUsage() + ', ')
        f.write(currentCPU + ', ')
        f.write(getRAMUsage())
        f.write(' }')

    sleep( intervalSeconds - intervalCPUCalc )

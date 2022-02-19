import argparse
from genericpath import exists
from shutil import disk_usage
from psutil import cpu_percent, virtual_memory, boot_time
from time import sleep, time
from datetime import datetime, timedelta
from socket import gethostname
from os import path
import json

# help menu
parser = argparse.ArgumentParser(
    description = 'Writes system usage information to JSON file on a timer. Use pythonw to run in background.',
    epilog='Quickstart: pythonw monitorSystem.py /path/to/homey-config-folder /')
parser.add_argument('filePath', metavar='path', type=str, nargs=1,
    help='Output directory i.e. /home/bob/homey-data')
parser.add_argument('disks', metavar='disks', type=str, nargs='+',
    help='Space-separated list of mount points to monitor (i.e. / /mnt/backups /mnt/media/work-ssd)')
parser.add_argument('--interval', metavar='N', type=int, nargs=1, default=30,
    help='Query system & update file every N seconds (default: 30)',)
parser.add_argument('--cpu_window', metavar='N', type=int, nargs=1, default=6,
    help='Average CPU usage over N seconds (default: 6)')

# byte -> mb/gb calculation
MB = 2**20
GB = 2**30

# get free, available, & total space for each disk in args.disks
def getDiskUsage():
    if len(args.disks) < 1:   return

    diskUsage = []
    for d in args.disks:
        if d.split() == []: continue
        
        total, used, free = disk_usage(d)
        diskUsage.append(formatDiskLine(d, total, used, free))
    return diskUsage

# average CPU usage over args.cpu_window seconds
# blocks for args.cpu_window seconds
def getCPUUsage():
    return str(cpu_percent(args.cpu_window))

# get system uptime
def getUptime():
    secondsUp = time() - boot_time()
    uptime = datetime(1,1,1) + timedelta(seconds=secondsUp)
    toReturn = ''

    # construct intelligent uptime string
    if uptime.day-1 > 0:
        toReturn += ('%d day' % (uptime.day-1))
        if uptime.day-1 < 2:
            toReturn += ', '
        else:
            toReturn += 's, '
    if uptime.hour > 0:
        toReturn += ('%d hours, ' % uptime.hour)
    toReturn += ('%d minutes' % uptime.minute)

    return toReturn

# return mem usage values formatted in MB
def getRAMUsage():
    raw = virtual_memory()

    return {
        "total": round(raw[0] / MB),
        "free":  round(raw[1] / MB),
        "used": round(raw[3] / MB),
        "percent_used": raw[2]
    }

# convert byte disk usage vaalues to GB
def formatDiskLine(label, total, used, free):
    return {
        "label":  label.replace(":", ""),
        "total": total // GB,
        "used":  used // GB,
        "free":  free // GB,
        "percent_used": round((used / total) * 100)
    }

# entrypoint
args = parser.parse_args()
dataFile = path.join(args.filePath[0], 'local_machine_data.json')

if args.interval < args.cpu_window:
    print('Error: cpu_window must be shorter than interval')
    exit(1)

while(True):
    data = {
        "hostname": gethostname(),
        "uptime": getUptime(),
        "cpu": getCPUUsage(),       # blocks for args.cpu_window seconds
        "ram": getRAMUsage(),
        "disks": getDiskUsage()
    }

    with open(dataFile, "w") as f:
        f.write(json.dumps(data, indent=4))

    print(json.dumps(data, indent=4))
    print(str(datetime.now()) + ' :: Successfully wrote to ' + dataFile)

    sleep( args.interval - args.cpu_window )   # compensate for CPU calc block

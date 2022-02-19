import argparse #    '||
import shutil #       || ..     ...   .. .. ..     ....  .... ...
import json #         ||' ||  .|  '|.  || || ||  .|...||  '|.  |
import os #           ||  ||  ||   ||  || || ||  ||        '|.|
import time #        .||. ||.  '|..|' .|| || ||.  '|...'    '|
import socket #                                          .. |
import psutil #            https://github.com/vlfldr      ''
import datetime    
IN_WINDOWS = os.name == 'nt'
if IN_WINDOWS:  import win32api

# help menu
parser = argparse.ArgumentParser(
    description = 'Writes system usage information to JSON file on a timer. Use pythonw to run in background.',
    epilog='Quickstart: pythonw monitorSystem.py /path/to/homey-config-folder /')
parser.add_argument('filePath', metavar='path', type=str, nargs=1,
    help='Output directory (relative or absolute)')
parser.add_argument('disks', metavar='disks', type=str, nargs='+',
    help='Space-separated list of mount points to monitor (i.e. / /mnt/backups /mnt/media/work-ssd).\
            On Windows: C:\\ E:\\ Z:\\')
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
        
        total, used, free = shutil.disk_usage(d)
        diskUsage.append(formatDiskLine(d, total, used, free))
    return diskUsage

# average CPU usage over args.cpu_window seconds
# blocks for args.cpu_window seconds
def getCPUUsage():
    return str(psutil.cpu_percent(args.cpu_window))

# get system uptime
def getUptime():
    secondsUp = time.time() - psutil.boot_time()
    uptime = datetime.datetime(1,1,1) + datetime.timedelta(seconds=secondsUp)
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
    raw = psutil.virtual_memory()

    return {
        "total": round(raw[0] / MB),
        "free":  round(raw[1] / MB),
        "used": round(raw[3] / MB),
        "percent_used": raw[2]
    }

# retrieve drive label & convert disk usage values to GB
def formatDiskLine(label, total, used, free):
    if IN_WINDOWS and win32api.GetVolumeInformation(label)[0] != "":
        label = win32api.GetVolumeInformation(label)[0]
    elif label != "/":
        if label[-1:] == '/':
            label = label[:-1]
        label = label.rsplit("/")[-1]
        
    print(label.rsplit("/"))
    return {
        "label":  label,
        "total": total // GB,
        "used":  used // GB,
        "free":  free // GB,
        "percent_used": round((used / total) * 100)
    }

# entrypoint
args = parser.parse_args()
dataFile = os.path.join(args.filePath[0], 'local_machine_data.json')

if args.interval < args.cpu_window:
    print('Error: cpu_window must be shorter than interval')
    exit(1)

while(True):
    data = {
        "hostname": socket.gethostname(),
        "uptime": getUptime(),
        "cpu": getCPUUsage(),       # blocks for args.cpu_window seconds
        "ram": getRAMUsage(),
        "disks": getDiskUsage()
    }

    with open(dataFile, "w") as f:
        f.write(json.dumps(data, indent=4))

    print(json.dumps(data, indent=4))
    print(str(datetime.datetime.now()) + ' :: Successfully wrote to ' + dataFile)

    time.sleep( args.interval - args.cpu_window )   # compensate for CPU calc block

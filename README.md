# homey
<p align="center">
  <img width="1080px" src="https://github.com/vlfldr/homey/blob/master/screenshot.png?raw=true" alt="homey dashboard"/>
</p>

Homey is a simple home server dashboard packed with functionality. The layout is loosely inspired by [Homer](https://github.com/bastienwirtz/homer).

<!-- TOC -->
- [Features](#features)
- [Installation & Configuration](#installation--configuration)
  - [Docker](#docker)
  - [Linux](#linux)
  - [Windows](#windows)
- [System Monitor Module](#system-monitor-module)
- [Docker Backends](#docker-backends)
- [Flood](#flood)
- [Minimal Mode](#minimal-mode)
- [Icons](#icons)
- [Configuration Options](#configuration-options)
- [Planned Features](#planned-features)
- [Built With](#built-with)
<!-- /TOC -->

**In development - please report all bugs!**

## Features

* Local Docker container management
* Remote Docker container management via [Portainer](https://github.com/portainer/portainer)
* Torrent transfer speed & download notifications via [Flood](https://github.com/jesec/flood/) 
  * *supported clients: qBittorent, rTorrent, Transmission, Deluge*
* Hourly & daily weather forecasts via [Open Meteo](https://open-meteo.com/en)
* Monitor up/down status of services
* Monitor server's CPU usage, RAM usage, disk usage, uptime
* Tablet & mobile layouts
* GUI configuration
* Easter eggs 🥚 👀

## Installation & Configuration
Supported platforms:
- Docker (Linux & Windows)
- Linux x86

Running on Windows without Docker is not currently supported. ARM has not been tested.

### Docker
1. Create a directory for config files: `mkdir ~/homey-data`
2. Download `docker-compose.yml`, `.env.example`, and `config.yml.example` from the [Releases](https://github.com/vlfldr/homey/releases) page or above. Place in newly created directory.
3. Configure external integrations in `.env.example`. Leave fields blank to disable. Once satisfied, rename to `.env`.

    - *Refer to [Docker Backends](#docker-backends) section to configure Docker/Portainer API access*
4. Configure UI options if desired in `config.yml.example` and rename to `config.yml`. Defaults should work out of the box.

    - *These options can be changed while homey is running.*
5. Map both volumes to the config folder and set homey's port (default 9080) in `docker-compose.yml`.
6. Ensure `docker-compose.yml` and `.env` are in the same directory. It's easiest to keep all three files in the config folder.
7. (Optional) Create a subdirectory for icons and populate it: `mkdir ~/homey-data/icons`

    - *Icons are **not** required for each service*
    - *Icons can also be added while homey is running or uploaded via GUI*
8. (Optional) Download and run `monitorSystem.py` to enable host machine stats. See [System Monitor Module](#system-monitor-module).
9. In the original directory: `docker-compose up -d`

### Linux
Prerequisites:
- Python 3 
- Node.js 16.14+
- npm 8.3.1+

1. Clone the repository: `git clone https://github.com/vlfldr/homey && cd homey`
2. Install dependencies:
```
python3 -m pip install -r homey-api/requirements.txt
cd homey && npm i
```
3. Follow steps 3-8 of Docker configuration. Key differences:

    - Keep `.env` in the project root
    - Edit `config.yml` in `homey-api/config` instead of an arbitrary docker volume
    - At the bottom of `.env` set `HOMEY_API_RUNNING_IN_DOCKER=False`

5. In the project root: `./run.sh`

### Windows
**Under Construction**


If you're running homey on a Windows host and wish to use the local Docker API backend, modify `docker-compose.yml` as follows:

    ...
    volumes:
      - //var/run/docker.sock://var/run/docker.sock
    ...

This will allow homey to view and control containers on the host machine. It's safe to ignore `HOMEY_API_DOCKER_USER_ID` and `GROUP_ID`.

## System Monitor Module

Displays CPU/RAM/disk usage and uptime. By design, Docker containers do not have access to detailed host information. This can be circumvented by **running a script on the host**: `monitorSystem.py`

- Download the script from the [Releases](https://github.com/vlfldr/homey/releases) page or above
- Place anywhere (does not have to be in config directory)
- Install process utilities: `pip install psutil`
- Run in background: `pythonw monitorSystem.py /path/to/homey-config-dir /`

  - This will write stats to file every 30 seconds and monitor disk usage on the OS drive.
- Launch homey


To monitor aditional drives, add them to the launch command: `pythonw monitorSystem.py /path/to/homey/config-dir / /mnt/backups /mnt/media/work-ssd`

Change file write frequency: `--interval 30`

Reference:
```
monitorSystem.py [-h] [--interval N] [--cpu_window N] path disks [disks ...]

Writes system usage information to JSON file on a timer.

positional arguments:
  path            Output directory i.e. /home/bob/homey-data
  disks           Space-separated list of mount points to monitor (i.e. / /mnt/backups /mnt/media/work-ssd)

optional arguments:
  -h, --help      show this help message and exit
  --interval N    Query system & update file every N seconds (default: 30)
  --cpu_window N  Average CPU usage over N seconds (default: 6)
```


## Docker Backends
**Portainer** - Communicates with a running [Portainer](https://github.com/portainer/portainer) instance. Preferred for its additional security (SSL password authentication). Its API should be accessible with no additional configuration at the same port as the web UI (default 9443).

- *Note: If using a self-signed cert, ignore self-signed warnings*

**Docker API** - Communicates with the parent Docker Engine process if running in a container. Talks to the local Docker Engine if running on bare metal. To find the appropriate config values for `.env`:
- User ID: `id -u`
- Docker group ID: `getent group docker | cut -d: -f3`
- Docker socket path: `/var/run/docker.sock` (unless you've changed it)

## Flood
[Flood](https://github.com/jesec/flood/) is a web-based frontend for multiple torrent clients. Once it's running and talking to your client of choice, the API should be accessible via the same port as the web UI. No additional configuration is required.

*Note: Unless you've deployed Flood with an SSL cert or behind a reverse proxy, credentials will be transmitted in plaintext upon authentication. **This should not pose a security risk as Flood only exposes its interfaces on the 127.0.0.1 by default.** However do be aware that someone snooping through local network traffic could theoretically obtain your Flood username & password.*

## Minimal Mode
**Minimal mode** turns homey into a more traditional dashboard with links to services and low overhead. Everything is disabled except service links and bookmarks. If you'd like to run homey in minimal mode and are not running in Docker, work with the local config file: `/public/config/config.yml`. If you're running in Docker, edit the config file in homey's Docker volume as usual. 

This option can be toggled using the settings menu or the `minimal_mode` flag.  

*Note: Once switched on, minimal mode can only be disabled by editing `config.yml`.*

## Icons
Homey looks for service icons in `<docker_volume>/icons` and `/public/data/icons`. Icons can also be uploaded via GUI in the settings menu. **Currently only PNG is supported.** 

Docker containers will use icons which share their exact name. For example: to set `portainer-agent`'s icon, upload a new icon named `portainer-agent.png`.

You can find a collection of PNG self-hosted service icons at NX211's [Homer Icons](https://github.com/NX211/homer-icons) (512x512) or [Homer Icons Compressed](https://github.com/vlfldr/homer-icons) (128x128). 

## Configuration Options
**Frontend** - *config.yml*

These options can all be modified through the GUI settings menu.

Option | Type | Purpose
---|---|---
title | String | Change the title of your dashboard
minimal_mode | Boolean | Disables 3D eyecandy and most functionality. See [Minimal Mode](#minimal-mode) for more info.
show_house | Boolean | Disables 3D house in header
compact_services | Boolean | Reduces padding around services
enable_service_status | Boolean | Toggles service up/down indicators
enable_notifications | Boolean | Toggles in-page notifications
audio_notifications | Boolean | Toggles in-page notification audio
bookmarks_in_header | Boolean | Fills empty space in the header with bookmarks
docker_api_backend | String | Docker display/control backend. Valid options: `docker`, `portainer`
service.name | String | Service display name
service.subtitle | String | Service description
service.url | String | Service URL
service.icon | String | Service icon filename without path i.e. `portainer.png`
bookmark.name | String | Bookmark display name
bookmark.url | String | Bookmark target URL
bookmark.hover | String | Optional hovertext for bookmarks 
card.enabled | Boolean | Toggles visibility of individual cards in bottom right section

**Backend** - *.env*

These settings cannot be changed after launching homey. **All floats and strings must be wrapped in double quotes**.

Option | Type | Purpose
----|----|----
TZ | String | Accepts a standard unix tz value i.e. `"America/Chicago"`. Ensures container's clock matches local clock. [List of all valid tz strings](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
HOMEY_API_WEATHER_LAT | String | Float with up to four decimal places i.e. `"23.4809"`. Sent to [Open Meteo](https://open-meteo.com/en/docs) weather API. *If location seems incorrect, double check +/- signs.*
HOMEY_API_WEATHER_LONG | String | Float with up to four decimal places. Sent to [Open Meteo](https://open-meteo.com/en/docs) weather API.
HOMEY_API_DOCKER_USER_ID | Integer | The user ID of an appropriately priveleged member of the `docker` group. See [Docker Backends](#docker-backends) for more info.
HOMEY_API_DOCKER_GROUP_ID | Integer | The group ID of the `docker` group. See [Docker Backends](#docker-backends) for more info.
HOMEY_API_DOCKER_SOCKET | String | Custom socket paths are not supported yet - do not modify this value. See [Docker Backends](#docker-backends) for more info.
HOMEY_API_PORTAINER_URL | String | Portainer URL including protocol & port i.e. `"https://192.168.1.2:9443"`
HOMEY_API_PORTAINER_USER | String | Portainer username
HOMEY_API_PORTAINER_PASSWORD | String | Portainer password
HOMEY_API_FLOOD_URL | String | Flood URL including protocol & port
HOMEY_API_FLOOD_USER | String | Flood username
HOMEY_API_FLOOD_PASSWORD | String | Flood password
HOMEY_API_RUNNING_IN_DOCKER | Boolean | Set to false if not running in Docker

## Planned Features
- ruTorrent support
- In-page notifications for flood downloads
- Color configuration
- Additional cards

## Built With:

* [Vue.js](https://github.com/vuejs/vue)
* [Three.js](https://github.com/mrdoob/three.js/)
* [Tween.js](https://github.com/tweenjs/tween.js)
* [Chart.js](https://github.com/chartjs/Chart.js)
* [SASS](https://github.com/sass/sass)
* [Flask](https://github.com/pallets/flask)
* ❤️

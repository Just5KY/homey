# homey
<p align="center">
  <img width="1080px" src="https://github.com/vlfldr/homey/blob/master/screenshot.png?raw=true" alt="homey dashboard"/>
</p>

Homey is a simple home server dashboard packed with functionality. The layout is loosely inspired by [Homer](https://github.com/bastienwirtz/homer).

**[Demo Video](https://odysee.com/homey-demo)**

<!-- TOC -->
- [Features](#features)
- [Installation & Configuration](#installation--configuration)
  - [Docker](#docker)
  - [Docker for Windows](#docker-for-windows)
  - [GNU/Linux](#gnulinux)
- [System Monitor Module](#system-monitor-module)
- [Docker Backends](#docker-backends)
- [Flood](#flood)
- [Minimal Mode](#minimal-mode)
- [Icons](#icons)
- [Configuration Options](#configuration-options)
- [Planned Features](#planned-features)
- [Other Things Called "Homey"](#other-things-called-homey)
- [Built With](#built-with)
<!-- /TOC -->

## Features

* Local Docker container management
* Remote Docker container management via [Portainer](https://github.com/portainer/portainer)
* Torrent transfer speed & download notifications via [Flood](https://github.com/jesec/flood/) 
  * *supported clients: qBittorent, rTorrent, Transmission, Deluge*
* Hourly & daily weather forecasts via [Open Meteo](https://open-meteo.com/en)
* Monitor up/down status of services
* Monitor server's CPU usage, RAM usage, disk usage, uptime
* Tablet & mobile layouts
* Easter eggs 🥚 👀

## Installation & Configuration
Supported platforms:
- [Docker](#docker)
- [Docker Desktop for Windows](#docker-for-windows)
- [GNU/Linux](#gnulinux)

Untested platforms:
- Windows (no Docker)
- Docker Desktop for Mac

*In theory, homey can run with minimal modification anywhere node & python are installed.*

**In development - bug reports welcome from all platforms!**

### Docker
1. Download `homey-data.zip` from the [Releases](https://github.com/vlfldr/homey/releases) page.
2. Unzip to a permanent location. This is where homey's config files and icons will be stored.
3. Configure integrations in `dotenv.example`. Rename to `.env`.
4. Configure UI options in `config.yml.example`. Rename to `config.yml`.
5. *(Optional) Edit homey's port (defualt 9080) in `docker-compose.yml`*
6. *(Optional) Add service icons to the `icons` subdirectory.*
7. *(Optional) Run [monitorSystem.py](#system-monitor-module) to enable host machine stats.*
8. Launch with: `docker-compose up -d`

Folder structure visualization:
```
homey-data
│   .env
│   config.yml  
│   docker-compose.yml  
└───icons
    │   homey.png
    │   portainer.png
    │   ...
    └───────────────
```
Notes:

  - See [Configuration Options](#configuration-options) for a description of each option
  - If homey fails to launch, ensure `.env` (**not dotenv**) is located in the same directory as `docker-compose.yml`
  - Leave `.env` values blank to disable
  - Refer to [Docker Backends](#docker-backends) to configure Docker/Portainer API access
  - `config.yml` defaults work out of the box
    - *These options can be changed while homey is running*
  - Icons can also be added while homey is running, via the options menu or `icons` folder
    - *Icons are **not** required for each service*
  - Config dir does **not** have to remain named homey-data
  - When running inside Docker, 0.0.0.0/localhost/127.0.0.1 resolve to the container's IP address - not the host's. To add services running on the host, use the machine's explicit local IP (i.e. 192.168.1.XX) instead.
  - Refer to [System Monitor Module](#system-monitor-module) for more information on `monitorSystem.py`


### Docker for Windows
The Docker socket and its permissions differ slightly on Windows.
1. In `docker-compose.yml`, add an extra slash to the host (first) Docker socket path:
```
  - //var/run/docker.sock:${HOMEY_API_DOCKER_SOCKET}
```
2. Replace `"${HOMEY_API_DOCKER_USER_ID}:${HOMEY_API_DOCKER_GROUP_ID}"` with `root`:
```
  user: root
```
3. Save & exit
4. (Optional) Remove the unused USER_ID & GROUP_ID lines from your .env file
5. Follow [Docker](#docker) setup instructions.

*Volume Mapping Note: The tilde character (~) maps to C:\Users\\\<you> on Windows.*

### GNU/Linux
Not recommended - the Docker images were created to orchestrate serving the frontend/backend, proxy rewrite rules, sharing resources, keeping track of gunicorn, etc. so you don't have to do so manually.

Prerequisites:
- Python 3 
- Node.js 16.14+
- npm 8.3.1+
- An http server of your choosing with proxy support
  - *Sample NGINX configuration can be found in the [client folder](homey/nginx.conf)*
 
1. Clone the repository: `git clone https://github.com/vlfldr/homey && cd homey`
2. Install dependencies:
```
python3 -m pip install -r homey-api/requirements.txt
cd homey && npm i
```
3. Configure external integrations in `.env.example`. Leave fields blank to disable. Rename to `.env`.
4. Configure UI options if desired in `homey-api/config/config.yml.example` and rename to `config.yml`.
5. (Optional) Copy icons into `homey/public/data/icons`
6. (Optional) Download and run `monitorSystem.py` to enable host machine stats. See [System Monitor Module](#system-monitor-module).
7. Build frontend:
```
cd homey
npm run prod_compile:sass
npm run build
```
8. Run backend: 
```
cd homey-api
gunicorn -b 0.0.0.0:9101 --threads 4 --worker-class gthread --log-file - app:app
```
*Note: If pip didn't automatically add gunicorn to $PATH, try:*
```
export PATH="$PATH:/user/<you>/.local/bin"
```
9. Serve the `/dist` folder however you like. Quick 'n' dirty:
```
sudo nginx -c '/path/to/downloaded/nginx.conf'
```
- *Sample NGINX configuration can be found in the [client folder](homey/nginx.conf)*

Folder structure must remain as follows:
```
homey
│   .env
├───homey
│   └───dist
├───homey-api
    └───config
        │   config.yml
        └────────────
```
Icons are uploaded to & managed through `/dist/data/icons` after building.

*Note: If you just want to check out the project but don't want to bother with Docker or NGINX, follow steps 1-6 and then run `./run-dev.sh` in the project root. This is not only insecure, it's over 10x heavier than it needs to be with all the development dependencies bundled in! **Do not run homey as a dashboard this way.***

## System Monitor Module

Displays CPU/RAM/disk usage and uptime. By design, Docker containers do not have access to detailed host information. This can be circumvented by **running a script on the host**: `monitorSystem.py`

- Download `monitorSystem.py` from the [Releases](https://github.com/vlfldr/homey/releases) page or above
- Place anywhere (does not have to be in config directory - can be)
- Install dependencies: `pip install psutil`
- Run in background: `pythonw monitorSystem.py /path/to/homey-config-dir /`

  - This will write stats to file every 30 seconds and monitor disk usage on the OS drive.
- Launch homey

To monitor aditional drives, add them to the launch command: `pythonw monitorSystem.py /path/to/homey/config-dir / /mnt/backups /mnt/media/work-ssd`

Change file write frequency: `--interval 30`

Reference:
```
usage: monitorSystem.py [-h] [--interval N] [--cpu_window N] path disks [disks ...]

Writes system usage information to JSON file on a timer. Use pythonw to run in background.

positional arguments:
  path            Output directory i.e. /home/bob/homey-data
  disks           Space-separated list of mount points to monitor. Examples:
                    Linux: / /mnt/backups /mnt/media/work-ssd 
                    Windows: C:\ E:\ Z:\

optional arguments:
  -h, --help      show this help message and exit
  --interval N    Query system & update file every N seconds (default: 30)
  --cpu_window N  Average CPU usage over N seconds (default: 6)

Quickstart: pythonw monitorSystem.py /path/to/homey-config-folder /
```

## Docker Backends
**Portainer** - Communicates with a running [Portainer](https://github.com/portainer/portainer) instance. Provides SSL password authentication. Its API should be accessible with no additional configuration at the same port as the web UI (default 9443).

- *Note: If using a self-signed cert, ignore self-signed warnings*

**Docker API** - Communicates with the parent Docker Engine process if running in a container. Talks to the local Docker Engine if running on bare metal. To find the appropriate config values for `.env`:
- User ID: `id -u`
- Docker group ID: `getent group docker | cut -d: -f3`
- Docker socket path: `/var/run/docker.sock` (unless you've changed it)

## Flood
[Flood](https://github.com/jesec/flood/) is a web-based frontend for multiple torrent clients. Once it's running and talking to your client of choice, the API should be accessible via the same port as the web UI. No additional configuration is required.

*Note: Unless you've deployed Flood with an SSL cert or behind a reverse proxy, credentials will be transmitted in plaintext upon authentication. **This should not pose a security risk as Flood only exposes its interfaces on 127.0.0.1 by default.** However do be aware that someone snooping through local network traffic could theoretically obtain your Flood username & password.*

## Minimal Mode
**Minimal mode** turns homey into a more traditional dashboard with links to services and low overhead. Everything is disabled except service links and bookmarks. If you'd like to run homey in minimal mode and are not running in Docker, work with the local config file: `/public/config/config.yml`. If you're running in Docker, edit the config file in homey's Docker volume as usual. 

This option can be toggled using the settings menu or the `minimal_mode` flag.  

*Note: Once switched on, minimal mode can only be disabled by editing `config.yml`.*

## Icons
Homey looks for service icons in `<docker_volume>/icons` and `homey/public/data/icons`. Icons can also be uploaded via GUI in the settings menu. **Currently only PNG is supported.** 

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

## Planned Features
- ruTorrent support
- More fine-grained control over torrents
- In-page notifications for flood downloads
- Color configuration
- Additional cards

## Other Things Called "Homey"
A few other (very cool) projects have already coined the name "homey", including a [home automation](https://homey.app) solution, an [apartment rental](https://www.homey.com.ro/) service, and a [children's budget management](https://www.homeyapp.net/) app. 

This project is in need of different title - open to suggestions!

## Built With

* [Vue.js](https://github.com/vuejs/vue)
* [Three.js](https://github.com/mrdoob/three.js/)
* [Tween.js](https://github.com/tweenjs/tween.js)
* [Chart.js](https://github.com/chartjs/Chart.js)
* [SASS](https://github.com/sass/sass)
* [Flask](https://github.com/pallets/flask)
* Modified [Moby Dock 3D Model](https://sketchfab.com/3d-models/moby-dock-docker-whale-b706010291ca46ad8daca2d4aeb79edd) by Maurice Svay ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/))
* ❤️

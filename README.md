# homey
<p align="center">
  <img src="https://github.com/vlfldr/homey/blob/master/screenshot.png?raw=true" alt="homey dashboard"/>
</p>

Homey is a simple home server dashboard packed with functionality. The layout is loosely inspired by [Homer](https://github.com/bastienwirtz/homer).

**Work in progress! Not ready yet.**

## Features

* Local Docker container management
* Remote Docker container management via [Portainer](https://github.com/portainer/portainer)
* Torrent transfer speed & download notifications via [Flood](https://github.com/jesec/flood/) 
  * *supported clients: qBittorent, rTorrent, Transmission, Deluge*
* Hourly & daily weather forecast
* Monitor up/down status of services
* Monitor server's CPU usage, RAM usage, disk usage, uptime
* Tablet & mobile layouts
* GUI configuration
* Easter eggs 🥚👀

## Installation & Configuration

When the project is released, docker images and better documentation will be provided. If you want to check it out beforehand:

    git clone https://github.com/vlfldr/homey
    cd homey
    
    mkdir ~/<docker_volume>
    cp .env.example .env
    cp homey-api/config/config.yml.example ~/<docker_volume>/config.yml

    <edit .env>
    <edit config.yml>
    <edit docker-compose.yml>

    docker-compose up

IMPORTANT: Unless you've deployed Flood with an SSL cert or behind a reverse proxy, credentials will be transmitted in plaintext upon authentication. **This should not be an issue as Flood only exposes its API/login page on 127.0.0.1 by default.** However do be aware that someone snooping through local network traffic could obtain your `HOMEY_API_FLOOD_USER` & `HOMEY_API_FLOOD_PASSWORD`.

### System monitor module

Displays CPU/RAM/disk usage and uptime. Docker containers cannot query the host for this information (for security reasons). This can be circumvented by **running a script on the host**: `monitorSystem.py`

- Put the script anywhere
- Install process utilities: `pip install psutil`
- Point `dataFile` at homey's config Docker volume
    - Or at `homey-api/config` if running outside of Docker
- Add mount points to `watchedDisks` to enable space usage reports
- Save & run in background with `pythonw monitorSystem.py`
- Launch homey

### Docker backends
**Portainer** - Communicates with a running [Portainer](https://github.com/portainer/portainer) instance. Preferred as it protects container access behind SSL password authentication.
- Ensure your target instance is reachable via https at the url provided in `.env`
- Portainer's default port is **9443**
- Don't worry about self-signed cert warnings

**Docker API** - Communicates with the parent Docker Engine process if running in a container. Communicates with the local Docker Engine process otherwise. To find the appropriate config values for `.env`:
- User ID: `id -u`
- Docker group ID: `getent group docker | cut -d: -f3`
- Docker socket path: `/var/run/docker.sock` (unless you've changed it)

### Windows

If you're running homey on a Windows host and wish to use the local Docker API backend, modify `docker-compose.yml` as follows:

    ...
    volumes:
      - //var/run/docker.sock://var/run/docker.sock
    ...

This will allow homey to view and control containers on the host machine. It's safe to ignore `HOMEY_API_DOCKER_USER_ID` and `GROUP_ID`.

### Minimal mode
**Minimal mode** turns homey into a more traditional dashboard with links to services and low overhead. 3D eyecandy, service links, and bookmarks are disabled. If you'd like to run homey in minimal mode and are not running in Docker, work with the local config file: `/public/config/config.yml`. If you're running in Docker, edit the config file in homey's Docker volume as usual. 

This option can be toggled using the settings menu or the `minimal_mode` flag.  

*Note: Once switched on, minimal mode can only be disabled by editing `config.yml`.*

### Icons
Homey looks for service icons in <docker_volume>/icons and /public/data/icons. Icons can also be uploaded via GUI in the settings menu. **Currently only PNG is supported.** 

Docker containers will use icons which share their exact name. For example: to set `portainer-agent`'s icon, upload a new icon named `portainer-agent.png`.

You can find a collection of PNG self-hosted service icons at NX211's [Homer Icons](https://github.com/NX211/homer-icons) (512x512) or [Homer Icons Compressed](https://github.com/vlfldr/homer-icons) (128x128). 

## Planned features
- ruTorrent support
- Color configuration
- Additional cards?

## Built with:

* [Vue.js](https://github.com/vuejs/vue)
* [SASS](https://github.com/sass/sass)
* [Chart.js](https://github.com/chartjs/Chart.js)
* [Three.js](https://github.com/mrdoob/three.js/) & [Tween.js](https://github.com/tweenjs/tween.js)
* [Flask](https://github.com/pallets/flask)
* ❤️

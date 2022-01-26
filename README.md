# homey
<p align="center">
  <img src="https://github.com/vlfldr/homey/blob/master/screenshot.png?raw=true" alt="homey dashboard"/>
</p>

Homey is a simple home server dashboard packed with functionality. The layout is loosely inspired by [Homer](https://github.com/bastienwirtz/homer).



**Work in progress! Not ready yet.**

## Features

* Securely manage Docker containers (remote & local) via [Portainer](https://github.com/portainer/portainer)
* Manage local containers via the native Docker API
* View qBittorent/rTorrent/Transmission/Deluge realtime stats & download progress through [Flood](https://github.com/jesec/flood/) *(ruTorrent support will be added in the future)*
* Configure from web interface or with a simple YAML file
* View up/down status of services at a glance
* View host CPU, RAM, & disk usage
* Get hourly & weekly weather forecasts
* Watch your Docker containers stack up on the interactive whale!
* Play with 3D things that spin!

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

**NOTE: This is a work in progress. Editing configuration from the frontend inside Docker is not yet supported.**

### Minimal mode
**Minimal mode** turns homey into a more traditional dashboard with links to services and low overhead. API functionality (Docker/Portainer, Flood, weather, service checker, settings menu) is disabled along with 3D eyecandy. This option can be toggled using the settings menu or the `minimal_mode` flag in `config.yml`.

*Note: Settings cannot be changed from the web UI in minimal mode. Once it is switched on, all configuration (**including switching minimal mode off**) must be done manually through `config.yml`*

### Icons
Icons are loaded from <docker_volume>/icons (or /public/data/icons if not using Docker)). New icons can be added in bulk via this folder or uploaded using the built-in service editor. You can find a collection of PNG self-hosted service icons at NX211's [Homer Icons](https://github.com/NX211/homer-icons) (512x512) or my fork [Homer Icons Compressed](https://github.com/vlfldr/homer-icons) (128x128). Docker containers will use icons that are an exact name match.

## Built with:

* [Vue.js](https://github.com/vuejs/vue)
* [SASS](https://github.com/sass/sass)
* [Chart.js](https://github.com/chartjs/Chart.js)
* [Three.js](https://github.com/mrdoob/three.js/) & [Tween.js](https://github.com/tweenjs/tween.js)
* [Flask](https://github.com/pallets/flask)
* ❤️

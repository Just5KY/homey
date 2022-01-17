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

When the project is released, a docker image and better documentation will be provided. If you want to check it out before release:

    git clone https://github.com/vlfldr/homey
    cd homey
    mv .env.example .env
    mv homey/src/assets/config.yml.example homey/src/assets/config.yml

    <fill out .env & homey/src/assets/config.yml>
    <add service icons to homey/public/images/icons>

    docker-compose up

**NOTE: This is a work in progress and currently unstable. If any of the #required endpoints in the .env file are configured incorrectly or unreachable, the application will crash.**

### Minimal mode
**Minimal mode** turns homey into a more traditional dashboard with links to services and low overhead. API functionality (Docker/Portainer, Flood, weather, service checker, settings menu) is disabled along with 3D eyecandy. This option can be toggled using the settings menu or the `minimal_mode` flag in `config.yml`.

*Note: Homey has no way of writing updated config files to the disk in minimal mode. Once it is switched on, all configuration (**including switching minimal mode off**) must be done manually through `config.yml`*

### Icons
The `icon` field in `config.yml` points to homey/public/images/icons. New icons can be added via this folder or uploaded using the built-in service editor. You can find a huge collection of PNG self-hosted service icons at NX211's [Homer Icons](https://github.com/NX211/homer-icons) (512x512) or my fork [Homer Icons Compressed](https://github.com/vlfldr/homer-icons) (128x128). Docker containers will use icons that are an exact name match.

## Built with:

* [Vue.js](https://github.com/vuejs/vue)
* [SASS](https://github.com/sass/sass)
* [Chart.js](https://github.com/chartjs/Chart.js)
* [Three.js](https://github.com/mrdoob/three.js/) & [Tween.js](https://github.com/tweenjs/tween.js)
* [Flask](https://github.com/pallets/flask)
* ❤️

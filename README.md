# homey
<p align="center">
  <img src="https://github.com/vlfldr/homey/blob/master/screenshot.png?raw=true" alt="homey dashboard"/>
</p>

Homey is a simple home server dashboard packed with functionality. The layout is loosely inspired by [Homer](https://github.com/bastienwirtz/homer).

## Features

* Securely manage Docker containers remotely or locally via [Portainer](https://github.com/portainer/portainer)
* Alternatively, manage local Docker containers via the Docker API
* View qBittorent/rTorrent/Transmission/Deluge realtime stats & download progress through [Flood](https://github.com/jesec/flood/) *(ruTorrent support will be added in the future)*
* Add services with a simple YAML file
* Get hourly & weekly weather forecasts
* Watch your Docker containers stack up on the interactive whale!
* Play with a 3D spinning house!

## Installation & Configuration

When the project is released, a docker image and better documentation will be provided. If you want to check it out before release:

    git clone https://github.com/vlfldr/homey
    cd homey
    mv homey-api/disks.example.txt homey-api/disks.txt
    mv .env.example .env

    <edit .env to include your sensitive info>
    <edit homey/src/assets/config.yml to point to your services>

    docker-compose up

**NOTE: This is a work in progress and currently unstable. If any of the #required endpoints in the .env file are configured incorrectly or unreachable, the application will crash.**

## Built with:

* [Vue.js](https://github.com/vuejs/vue)
* [SASS](https://github.com/sass/sass)
* [Chart.js](https://github.com/chartjs/Chart.js)
* [Three.js](https://github.com/mrdoob/three.js/) & [Tween.js](https://github.com/tweenjs/tween.js)
* [Flask](https://github.com/pallets/flask)
* ❤️

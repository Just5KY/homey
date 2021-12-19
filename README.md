# homey
<p align="center">
  <img src="https://github.com/vlfldr/homey/blob/master/screenshot.png?raw=true" alt="homey dashboard"/>
</p>

## Work in progress! Not ready yet.

Homey is a simple home server dashboard loosely inspired by Homer. From one cozy page, you can:
* Manage (pause/start/stop/restart) docker containers locally via the Docker API or remotely via Portainer - no custom tags required.
* Manage torrents through Flood and view realtime upload/download stats
* Add services with a simple YAML file
* View weather forecasts
* Watch your services stack up on the interactive Docker whale
* Play with a 3D spinning house

**For most functionality (Docker/Portainer, Flood, weather, etc) homey-api is required.** 
*It is included by default in the install instructions and docker compose file. The dashboard will run without it (soon™, currently unstable), but without the api homey will be more of a glorified bookmark page.*

## Project setup
**When the project is released, official images will be pushed to Docker Hub.**

*Installation, configuration, and deployment instructions are for running homey via docker-compose. If you would prefer to run homey on metal or in a single container, feel free to do so.*

For now:
0. Clone this repository
1. Create an .env file based on .env.example. Place into root project directory next to docker-compose.yml.
  1a. Ensure the docker socket path, group ID, and user ID are correct. `getent group` to find docker's group ID.
3. Copy (not move) your .env file to the homey-api folder. *This step will be removed when configuration is streamlined.*
4. (in project root)$ docker-compose build
5. $ docker-compose up -d
6. Visit localhost:8080 to see homey :^)

**Please report any issues with this build on the issues page!**

## Built with:

* Vue (frontend, data binding)
* SASS (layout, theming)
* Three.js & Tween.js (eyecandy)
* Flask (backend)

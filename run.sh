#! /bin/bash

# local launch script for development/debugging
# the app will not launch unless .env and homey-api/disks.txt are configured correctly

# install requirements
# cd homey
# npm i
# cd ../homey-api
# pip install -r ./requirements.txt
cd homey-api

# run backend; capture process ID for exit
python ./app.py &
pid[0]=$!
# run frontend
cd ../homey && npm run dev &
pid[1]=$!

# kill both on interrupt
trap "kill ${pid[0]} ${pid[1]}; exit 1" INT
wait
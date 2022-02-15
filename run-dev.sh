#! /bin/bash

# local launch script for development

# install requirements
# cd homey && npm i && cd ../homey-api && pip install -r ./requirements.txt

cd homey-api

# copy config file to frontend (fallback)
cp ./config/config.yml ../homey/public/config

# run backend
python ./app.py &
pid[0]=$!
# run frontend
cd ../homey && npm run dev &
pid[1]=$!

# kill both on interrupt
trap "kill ${pid[0]} ${pid[1]}; exit 1" INT
wait
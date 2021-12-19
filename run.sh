#! /bin/bash

# install requirements & run locally
# the app will not launch unless .env and homey-api/disks.txt are configured correctly

cd homey
npm i
pip install -r ../homey-api/requirements.txt

python ../homey-api/app.py & npm run dev && kill $!
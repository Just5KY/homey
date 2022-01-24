FROM debian:bullseye-slim

# node:lts-alpine, standard practices                   965MB
# debian:bullseye-slim, manual node & npm management    277MB

# install node & npm
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    (curl -sL https://deb.nodesource.com/setup_16.x | bash -) && \
    apt-get install -y --no-install-recommends nodejs npm && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

WORKDIR /app

ENV NODE_ENV production

# copy source into container
COPY . .

# install node modules, compile SASS,
# build for production, remove intermediate files
RUN npm install --production && \
    npm run prod_compile:sass && \
    npm run build && \
    rm -rf ./node_modules

# install production http server
RUN npm install -g http-server

# serve on 8080
EXPOSE 8080
CMD ["http-server", "dist"]
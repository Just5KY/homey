FROM debian:bullseye-slim as build

# install node & npm
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    (curl -sL https://deb.nodesource.com/setup_16.x | bash -) && \
    apt-get install -y --no-install-recommends nodejs npm && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

WORKDIR /app
ENV NODE_ENV production

# copy source into build layer
COPY . .

# install node modules, compile SASS,
# build for production, remove intermediate files
RUN npm install --production && \
    npm run prod_compile:sass && \
    npm run build && \
    rm -rf ./node_modules


# final image - optimized for size
FROM node:16-alpine

WORKDIR /app

# copy only build output out of intermediate layer
COPY --from=build /app/dist .

# install production http server
RUN npm install -g http-server

# serve on 8080
EXPOSE 8080
CMD ["http-server", "."]
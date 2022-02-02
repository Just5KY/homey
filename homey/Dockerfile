FROM node:lts-slim as build

WORKDIR /app

ENV NODE_ENV production

COPY . .

RUN npm install --production && \
    npm run prod_compile:sass && \
    npm run build

# final image - optimized for size
FROM nginx:alpine

# this may break things - old file used /app workdir
#WORKDIR /usr/share/nginx/html
WORKDIR /app

# copy nginx config
COPY ./nginx.conf /etc/nginx/nginx.conf

# clean nginx default files
#RUN rm -rf ./*

# copy only build output out of intermediate layer
COPY --from=build /app/dist .

# serve on 8080
# EXPOSE 8080
ENTRYPOINT ["nginx", "-g", "daemon off;"]
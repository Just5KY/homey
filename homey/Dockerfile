FROM node:lts-alpine

RUN npm install -g http-server

WORKDIR /app

# install modules
COPY package*.json ./
RUN apk add --update --no-cache --virtual .gyp python3 make g++ 
RUN npm install
RUN apk del .gyp

# copy source into container
COPY . .

# compile sass -> css and build production
RUN npm run prod_compile:sass
RUN npm run build
RUN rm -rf node_modules/

# serve on 8080
EXPOSE 8080
CMD ["http-server", "dist"]
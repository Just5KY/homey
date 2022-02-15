FROM node:lts-slim as build

WORKDIR /app

COPY package*.json ./

RUN npm install 

COPY . .

ENV NODE_ENV production
    
RUN npm run --no-update-notifier prod_compile:sass && \
    npm run --no-update-notifier build 

# final image
FROM nginx:alpine

WORKDIR /app

# copy nginx config
COPY ./nginx.conf /etc/nginx/nginx.conf

COPY --from=build /app/dist .

# serve on 80
ENTRYPOINT ["nginx", "-g", "daemon off;"]
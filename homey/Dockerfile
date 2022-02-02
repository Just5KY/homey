FROM node:lts-slim as build

WORKDIR /app

COPY . .

ENV NODE_ENV production

# build production
RUN npm install --production && \
    npm run prod_compile:sass && \
    npm run build

# final image
FROM nginx:alpine

WORKDIR /app

# copy nginx config
COPY ./nginx.conf /etc/nginx/nginx.conf

COPY --from=build /app/dist .

# serve on 80
ENTRYPOINT ["nginx", "-g", "daemon off;"]
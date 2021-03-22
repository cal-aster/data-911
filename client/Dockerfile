# Author:  Meryll Dindin
# Date:    November 04, 2020
# Project: CalAster

# node environment
FROM node:latest as build
WORKDIR /app
COPY package*.json ./
RUN npm install npm@latest -g
RUN npm install --silent
COPY . .
ARG stage
RUN npm run ${stage}

# use compiled dist to build Nginx image
FROM nginx:stable-alpine as publish
LABEL maintainer="Meryll Dindin meryll@calaster.com"
WORKDIR /app
COPY --from=build /app/dist /app
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

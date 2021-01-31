# Author:  Meryll Dindin
# Date:    November 04, 2020
# Project: CalAster

# Setup node environment
# FROM node:lts as build

# Install packages and build Node image
# WORKDIR /app
# COPY package*.json ./
# RUN npm install --silent
# COPY . .
# ARG stage
# RUN npm run ${stage}

# Use previous dist to build Nginx image
FROM nginx:stable-alpine
LABEL maintainer="Meryll Dindin meryll@calaster.com"
RUN mkdir /app
COPY ./dist /app
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
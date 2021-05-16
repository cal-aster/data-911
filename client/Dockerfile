# node environment
FROM node:alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install npm@latest -g
RUN npm install --silent
COPY . .
RUN npm run build

# use compiled dist to build Nginx image
FROM nginx:stable-alpine as publish
LABEL maintainer="Meryll Dindin meryll@calaster.com"
WORKDIR /app
COPY --from=build /app/dist /app
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

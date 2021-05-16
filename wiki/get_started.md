# CalAster - Data911

## Clone our repository

```bash
git clone https://github.com/cal-aster/data-911
```

## Before launching

Make sure to build your `.env.development` in each folder on the basis of the provided `.env.example`.

## Start the backend

**server**: Backend python server, based on FastAPI.

```bash
cd data911/server
make install && make start
```

## Start the frontend

**client**: Front-end service for visualization, based on Vue.js and Vuetify.

```bash
cd data911/client
make install && make start
```

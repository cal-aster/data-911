# CalAster - Data911
`Author: Meryll Dindin`
`Contact: meryll@calaster.com`

## Get started
```bash
git clone https://github.com/cal-aster/data-911
```

## Ecosystem
* **client**: Front-end service for visualization, based on Vue.js and Vuetify.
* **server**: Backend python server, based on FastAPI.

## Before launching
Make sure to build your `.env.development` in each folder on the basis of the provided `.env.example`.

## [Port 8000] Server
```bash
cd data911/server
pip install -r requirements
uvicorn --reload main:app
```

## [Port 8080] Client
```bash
cd data911/client
npm install
npm run dev
```

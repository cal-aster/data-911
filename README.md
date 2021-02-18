# CalAster - Data911
`Author: Meryll Dindin`
`Contact: meryll@calaster.com`

## What is Data911?

The three-digit telephone number "9-1-1" has been designated as the "Universal Emergency Number" for citizens throughout the United States to request emergency assistance. It is intended as a nationwide telephone number and gives the public fast and easy access to a Public Safety Answering Point (PSAP). The intense interest in the concept of 9-1-1 can be attributed primarily to the recognition of characteristics of modern society, i.e., increased incidences of crimes, accidents, and medical emergencies, the inadequacy of existing emergency reporting methods, and the continued growth and mobility of the population. In the 9-1-1 world, the saying goes by "If you have seen a PSAP, then you have seen one PSAP." The direct consequences are that, among the 6000+ PSAPs out there, each one has a different approach to digitalization, making it excessively hard for engineers and data scientists to come up with analyses at scale. Our vision is first and foremost a visualization platform of standardized and unified 9-1-1 data streams, enabling others to come up with other ideas once the data is in a good enough place.

## Clone our repository
```bash
git clone https://github.com/cal-aster/data-911
```

## Before launching
Make sure to build your `.env.development` in each folder on the basis of the provided `.env.example`.

## [Port 8000] Server

**server**: Backend python server, based on FastAPI.

```bash
cd data911/server
pip install -r requirements
uvicorn --reload main:app
```

## [Port 8080] Client

**client**: Front-end service for visualization, based on Vue.js and Vuetify.

```bash
cd data911/client
npm install
npm run dev
```

# CalAster - Data911
`Author: Meryll Dindin`
`Contact: meryll@calaster.com`

## Get started
```bash
mkdir CalAster
cd CalAster
git clone https://github.com/cal-aster/data911
cd data911
python control.py config-project
source ./bin/activate
python control.py create-project
```

## Ecosystem
* **bastion**: Enable communication with AWS RDS while keeping it away from public internet.
* **client**: Core platform, for clients and DispoX's employees.
* **configs**: Required templates folder to feed in the creation of instances on AWS.
* **server**: Backend FastAPI core backend server.

## [Port 8000] Server
```bash
cd data911/server
docker build -t server .
docker run -it -p 8000:5000 --env-file=.env.development server
```

## [Port 8080] Client
```bash
cd data911/client
docker build -t client --build-arg stage=development .
docker run -it -p 8080:80 client
```

# Data911 - Bastion
`Author: Meryll Dindin`
`Contact: meryll@calaster.com`

## Project setup
```
source ../../bin/activate
pip install -r requirements.txt
pip install gunicorn uvicorn=0.11.8 python-socketio
pip install --upgrade setuptools
```

## Compiles and hot-reloads for development
```
source ../../bin/activate
uvicorn --reload main:wss
```

## Dockerize and run locally
```
docker build -t bastion .
docker run -it -p 8000:5000 --env-file=.env.development bastion
```

## Access to documentation

### Using redoc: http://localhost:8000/redoc

### Using swagger: http://localhost:8000/docs

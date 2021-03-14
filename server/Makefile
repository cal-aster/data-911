install:
	pip install --upgrade pip
	pip install --upgrade setuptools
	pip install -r requirements.txt

start:
	uvicorn --reload main:app

build:
	docker build -t data911/server:latest .

docker:
	docker run -it -p 8000:5000 --env-file=.devops/.env.development data911/server:latest

pull:
	docker pull data911/server:latest

deploy:
	docker build -t data911/server:latest .
	docker push data911/server:latest
	python ../control.py deploy-artifact production calaster

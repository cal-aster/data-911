directory=$(shell pwd)

install:
	pip install --upgrade pip
	pip install --upgrade setuptools
	pip install -r requirements.txt

start:
	uvicorn --reload main:app

docker:
	docker build -t calaster/data911:server_development .
	docker run -it -p 8000:5000 --env-file=.devops/.env.development -v $(directory):/app calaster/data911:server_development

push:
	docker build -t calaster/data911:server_development .
	docker push calaster/data911:server_development

pull:
	docker pull calaster/data911:server_development

push-prod:
	docker build -t calaster/data911:server_production .
	docker push calaster/data911:server_production

pull-prod:
	docker pull calaster/data911:server_production

deploy-prod:
	docker build -t calaster/data911:server_production .
	docker push calaster/data911:server_production
	python ../control.py deploy-artifact production calaster

end-prod:
	python ../control.py terminate production calaster

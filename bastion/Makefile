install:
	pip install --upgrade pip
	pip install --upgrade setuptools
	pip install -r requirements.txt

start:
	uvicorn --reload main:app

build-dev:
	docker build -t calaster/data911:bastion_development .

run-dev:
	make build-dev
	docker run -it -p 8000:5000 --env-file=.devops/.env.development calaster/data911:bastion_development

build-production:
	docker build -t calaster/data911:bastion_production .

run-production:
	docker run -it -p 8000:5000 --env-file=.devops/.env.production calaster/data911:bastion_production

push-production:
	make build-production
	docker push calaster/data911:bastion_production

create-production:
	make push-production
	python ../control.py create-artifact production calaster

deploy-production:
	make push-production
	python ../control.py deploy-artifact production calaster

end-production:
	python ../control.py terminate production calaster

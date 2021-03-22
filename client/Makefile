install:
	rm -rf node_modules/
	npm install

start:
	npm run dev

docker:
	docker build -t calaster/data911:client_development --build-arg stage=development .
	docker run -it -p 8080:80 calaster/data911:client_development

push:
	docker build -t calaster/data911:client_development --build-arg stage=development .
	docker push calaster/data911:client_development

pull:
	docker pull calaster/data911:client_development

push-prod:
	docker build -t calaster/data911:client_production --build-arg stage=production .
	docker push calaster/data911:client_production

pull-prod:
	docker pull calaster/data911:client_production

deploy-prod:
	docker build -t calaster/data911:client_production --build-arg stage=production .
	docker push calaster/data911:client_production
	python ../control.py deploy-artifact production calaster

end-prod:
	python ../control.py terminate production calaster

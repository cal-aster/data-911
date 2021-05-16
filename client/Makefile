install:
	rm -rf node_modules/
	npm install

start:
	npm run dev

start-dev:
	docker-compose up -d --build --remove-orphans client

build-dev:
	mkdir tmp/
	cp -r public/ src/ ./tmp
	cp Dockerfile nginx.conf package-lock.json package.json babel.config.js ./tmp
	cp .devops/.env.development ./tmp/.env
	docker build -t calaster/data911:client_development ./tmp
	rm -rf tmp/

run-dev:
	docker run -it -p 8080:80 calaster/data911:client_development

build-production:
	mkdir tmp/
	cp -r public/ src/ ./tmp
	cp Dockerfile nginx.conf package-lock.json package.json babel.config.js ./tmp
	cp .devops/.env.production ./tmp/.env
	docker build -t calaster/data911:client_production ./tmp
	rm -rf tmp/

start-production:
	make build-production
	docker run -it -p 8080:80 calaster/data911:client_production

push-production:
	make build-production
	docker push calaster/data911:client_production

create-production:
	make push-production
	python ../control.py create-artifact production polygon

deploy-production:
	make push-production
	python ../control.py deploy-artifact production polygon

end-production:
	python ../control.py terminate production polygon

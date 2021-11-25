# Environments
-include .env
AWS_URI = 427235730535.dkr.ecr.sa-east-1.amazonaws.com

run:
	yarn run serve

format:
	yarn run eslint --ext .js,.vue src --fix

docker:
	docker build -t projectstore-frontend .

release:
	@echo "Connecting into Docker account"
	@aws ecr get-login-password | docker login --username AWS --password-stdin $(AWS_URI)
	@echo "Input version[$(shell git describe --abbrev=0 --tags --always)]:"
	@read INPUT_VERSION;\
	echo "Creating a new release version: $$INPUT_VERSION";\
	docker build -t projectstore-frontend .;\
	docker tag projectstore-frontend $(AWS_URI)/projectstore-frontend:latest;\
	docker tag projectstore-frontend $(AWS_URI)/projectstore-frontend:$$INPUT_VERSION;\
	docker push $(AWS_URI)/projectstore-frontend:latest;\
	docker push $(AWS_URI)/projectstore-frontend:$$INPUT_VERSION

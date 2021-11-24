# Variables
-include .env
PYTHONPATH = $(shell pwd)
AWS_URI = 427235730535.dkr.ecr.sa-east-1.amazonaws.com


run:
	@poetry run uvicorn "src.app:app" --port 5000 --reload

deploy: upgrade
	@poetry run gunicorn src.app:app -c "./src/gunicorn.py"

test:
	@ENVIRONMENT=test poetry run pytest

docker:
	@docker rm -f store || true
	@docker build -t store .
	@docker run --expose 80 --env-file .env.docker --name=store --network=global-default -p 8000:80 -d store make deploy

format:
	@poetry run black src tests migration
	@poetry run isort src tests migration
	@poetry run autoflake8 --remove-unused-variables --recursive --exclude=__init__.py --in-place src tests migration
	@poetry run flake8 src tests migration

revision:
	@PYTHONPATH="${PYTHONPATH}" poetry run alembic revision --autogenerate

upgrade:
	@PYTHONPATH="${PYTHONPATH}" poetry run alembic upgrade head

downgrade:
	@PYTHONPATH="${PYTHONPATH}" poetry run alembic downgrade head

clean-pyc:
	@find . -name "__pycache__" -exec rm -rf {} +
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +

coverage:
	@poetry run coverage run -m pytest
	@poetry run coverage report -m
	@poetry run coverage html
	@wslview ./htmlcov/index.html || powershell.exe Invoke-Expression ./htmlcov/index.html || xdg-open ./htmlcov/index.html

release:
	@echo Loggin into container registry
	@aws ecr get-login-password | docker login --username AWS --password-stdin $(AWS_URI)
	@echo "Input version[$(shell git describe --abbrev=0 --tags --always)]:"
	@read INPUT_VERSION;\
	echo "Creating a new release version: $$INPUT_VERSION";\
	docker build -t projectstore-backend .;\
	echo "Tag image";\
	docker tag projectstore-backend $(AWS_URI)/projectstore-backend:latest;\
	docker tag projectstore-backend $(AWS_URI)/projectstore-backend:$$INPUT_VERSION;\
	echo "Push image to container registry";\
	docker push $(AWS_URI)/projectstore-backend:latest;\
	docker push $(AWS_URI)/projectstore-backend:$$INPUT_VERSION

# Variables
include .env
PYTHONPATH = $(shell pwd)

run:
	@uvicorn "src.app:app" --port 5000 --reload

deploy: upgrade
	@gunicorn src.app:app -c "./src/gunicorn.py"

test:
	@ENVIRONMENT=test pytest tests

docker:
	@docker rm -f store || true
	@docker build -t store .
	@docker run --name=store --network=global-default -p 8000:80 -d store

format:
	@black src tests migration
	@isort src tests migration
	@flake8 src tests migration

revision:
	@PYTHONPATH="${PYTHONPATH}" alembic revision --autogenerate

upgrade:
	@PYTHONPATH="${PYTHONPATH}" poetry run alembic upgrade head

downgrade:
	@PYTHONPATH="${PYTHONPATH}" alembic downgrade head

clean-pyc:
	@find . -name "__pycache__" -exec rm -rf {} +
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +

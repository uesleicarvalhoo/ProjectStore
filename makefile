# Variables
PYTHONPATH = $(shell pwd)

run:
	@uvicorn "src.app:app" --port 5000 --reload

test:
	ENV=test pytest tests

docker:
	@docker rm -f store || true
	@docker build -t store .
	@docker run --name=store --network=mysql-server-network -p 8000:80 -d store

format:
	@black src tests migration
	@isort src tests migration
	@flake8 src tests migration

revision:
	@PYTHONPATH="${PYTHONPATH}" alembic revision --autogenerate

upgrade:
	@PYTHONPATH="${PYTHONPATH}" alembic upgrade head

downgrade:
	@PYTHONPATH="${PYTHONPATH}" alembic downgrade 69ae8a7b14d3

clean-pyc:
	@find . -name "__pycache__" -exec rm -rf {} +
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +

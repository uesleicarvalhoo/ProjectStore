# Variables
-include .env
PYTHONPATH = $(shell pwd)

run:
	@poetry run uvicorn "src.app:app" --port 5000 --reload

deploy: upgrade
	@poetry run gunicorn src.app:app -c "./src/gunicorn.py"

test:
	@ENVIRONMENT=test pytest tests

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

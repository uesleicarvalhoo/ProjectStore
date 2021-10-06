FROM python:3.9-slim-buster

WORKDIR /srv

RUN apt update -y && apt upgrade -y && apt install -y make curl npm

RUN pip install poetry && poetry config virtualenvs.create false

RUN cp /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && \
    echo "America/Sao_Paulo" > /etc/timezone

ADD pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-dev --no-interaction --no-ansi

RUN npm install

ADD . .

EXPOSE 80

ENTRYPOINT ["gunicorn", "src.app:app", "-c", "./src/gunicorn.py"]

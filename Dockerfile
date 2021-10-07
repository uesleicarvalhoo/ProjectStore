FROM python:3.9-slim-buster

WORKDIR /srv

RUN apt update -y && apt upgrade -y && apt install -y make

RUN pip install poetry

RUN cp /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && \
    echo "America/Sao_Paulo" > /etc/timezone

ADD pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-dev --no-interaction --no-ansi

ADD . .

EXPOSE 80

ENTRYPOINT ["make", "deploy"]

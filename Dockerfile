FROM python:3.9-slim-buster

WORKDIR /app

RUN apt update -y && apt upgrade -y && apt install -y make curl npm

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

RUN cp /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && \
    echo "America/Sao_Paulo" > /etc/timezone

ADD pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-dev && npm install

ADD . .

EXPOSE 80

ENTRYPOINT ["gunicorn", "src.app:app", "-c", "./src/gunicorn.py"]

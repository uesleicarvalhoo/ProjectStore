FROM python:3.9-slim-buster

WORKDIR /app

RUN apt update -y && apt upgrade -y && apt install make curl -y

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

RUN cp /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && \
    echo "America/Sao_Paulo" > /etc/timezone

ADD pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-dev

ADD . .

EXPOSE 80

ENV PYTHONPATH=/app

ENTRYPOINT ["gunicorn", "src.app:create_app()", "-c", "./src/gunicorn.py"]

FROM tiangolo/meinheld-gunicorn-flask:python3.8-alpine3.11

COPY requirements.txt /app/requirements.txt
WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

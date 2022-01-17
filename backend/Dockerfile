FROM python:3.8.5-slim

WORKDIR /app

COPY ../requirements.txt .

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip3 install -r /app/requirements.txt

COPY ../ .

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:18000

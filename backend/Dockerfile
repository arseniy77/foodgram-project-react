FROM python:3.8.5-slim

#RUN mkdir /code
WORKDIR /code

COPY ../requirements.txt .

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip3 install -r /code/requirements.txt

COPY ../ .

#WORKDIR /code

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:18000

CMD python /code/manage.py runserver 0:18000
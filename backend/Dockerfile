# создать образ на основе базового слоя python (там будет Оd-tС и интерпретатор Python)
FROM python:3.8.5-slim

# создать директорию /code
RUN mkdir /code

# скопировать файл requirements.txt из директории, в которой лежит докерфайл, в директорию /code
COPY requirements.txt /code

# выполнить команду (как в терминале, с тем же синтаксисом) для установки пакетов из requirements.txt
RUN pip3 install -r /code/requirements.txt

# скопировать всё содержимое директории, в которой лежит докерфайл, в директорию /code
COPY . /code

WORKDIR /code

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000

# при старте контейнера выполнить runserver
CMD python /code/manage.py runserver 0:8000
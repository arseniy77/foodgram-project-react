# Foodgram-project
http://foodgram.arscorp.ru

Страница администратора http://foodgram.arscorp.ru/admin

логин: admin

пароль: admin

email администратора admin@admin.ru

## Описание
Приложение «Продуктовый помощник»: сайт, на котором пользователи публикуют рецепты, добавляют чужие рецепты в избранное и подписываются на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

Проект был выполнен в качестве дипломного задания в Яндекс Практикум.
## Стек технологий
- Python
- Django
- PostgreSQL
- Docker
- Nginx
- Gunicorn

## Как запустить проект, используя Docker (база данных PostgreSQL):
1) Клонируйте репозиторий с проектом:
```
git clone https://github.com/arseniy77/foodgram-project-react.git
```
2) В директории проекта создайте файл .env, по пути `<project_name>/backend/foodgram/.env`, в котором пропишите следующие переменные окружения:
 - SECRET_KEY = 'ваш secret-key'
 - ALLOWED_HOSTS = 'localhost,127.0.0.1,[::1],backend,web,"ваш сайт"'  # пробел не нужен
 - FROM_EMAIL = "ваш e-mail"
 - DB_ENGINE = 'django.db.backends.postgresql'
 - DB_NAME = 'postgres'
 - POSTGRES_USER = 'postgres'
 - POSTGRES_PASSWORD = "пароль базы данных"
 - DB_HOST = 'db'
 - DB_PORT = "порт базы данных"

##### Для локального использования DB_HOST=127.0.0.1
##### Для включения дебага DEBUG=True


3) С помощью Dockerfile и docker-compose.yaml разверните проект:

Для запуска:
1. После запуска контейнера Docker-Compose, выполните команду для первоначальной настройки:
`docker-compose exec web ./startup.sh`
2. После приглашения, введите данные учетной записи суперпользователя
3. Доступ в панель администратора возможен по адресу [sitename/admin/](http://127.0.0.1/admin/)

    Например: [http://127.0.0.1/admin/](http://127.0.0.1/admin/)
4. Если у вас есть файл с дампом базы данных, вы можете загрузить свою базу с помощью команды:

    `docker-compose exec python manage.py loaddata <имя файла>`
## Панель администрирования
http://127.0.0.1/admin/

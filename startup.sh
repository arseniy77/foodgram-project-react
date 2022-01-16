#!/bin/bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
echo "Creating Superuser account:"
python manage.py createsuperuser
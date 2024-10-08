#!/bin/sh

while ! nc -z database 5432; do
    sleep 0.1
done

python manage.py makemigrations

python manage.py migrate

python manage.py collectstatic --noinput

daphne -b 0.0.0.0 main.asgi:application

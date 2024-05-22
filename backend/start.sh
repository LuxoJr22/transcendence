# !/bin/sh

while ! nc -z database 5432; do
   sleep 1
done

python manage.py makemigrations

python manage.py migrate

python manage.py runserver 0.0.0.0:8000
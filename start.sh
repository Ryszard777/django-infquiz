#!/bin/sh
# Dodajemy pętle aby migracja napewno odpaliła się gdy baza jest gotowa na działanie
while ! nc -z db 5432; do
  sleep 1
done

python manage.py migrate --noinput

python manage.py collectstatic --noinput

exec "$@"

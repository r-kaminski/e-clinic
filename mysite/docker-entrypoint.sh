#!/bin/sh
set -e

sleep 1

python manage.py makemigrations
python manage.py migrate
python manage.py shell < populate-database.py

exec "$@"
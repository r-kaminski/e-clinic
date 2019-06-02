#!/bin/sh
set -e

sleep 1

python manage.py makemigrations
python manage.py migrate

exec "$@"
#!/bin/bash
set -oxu

python manage.py makemigrations $1
python manage.py sqlmigrate $1 $2
python manage.py migrate

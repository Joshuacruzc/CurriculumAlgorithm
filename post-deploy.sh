# !/usr/bin/env bash

echo "=> Performing database migrations..."
python manage.py makemigrations curriculum_algorithm
python manage.py migrate

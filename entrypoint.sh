#!/bin/bash

./wait-for-it.sh db:5432 --timeout=30 --strict -- echo "PostgreSQL is up"

echo "Applying migrations..."
python manage.py migrate

echo "Starting server..."
python manage.py runserver 0.0.0.0:8000

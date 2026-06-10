#!/bin/sh

set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput || true

echo "Starting Gunicorn..."
gunicorn marketplace.wsgi:application --bind 0.0.0.0:$PORT
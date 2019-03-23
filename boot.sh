#!/usr/bin/env bash
python manage.py db upgrade
exec gunicorn -b :5000 --access-logfile - --error-logfile - app:app

#!/usr/bin/env ash
cd /app
gunicorn --bind 0.0.0.0:5000 wsgi:flask_app
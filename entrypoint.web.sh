#!/bin/bash

set -e

echo "📦 Starting Django setup..."

# اعمال مایگریشن‌ها
python manage.py migrate --noinput

# جمع‌آوری فایل‌های استاتیک
python manage.py collectstatic --noinput

echo "🚀 Running Gunicorn..."
exec "$@"

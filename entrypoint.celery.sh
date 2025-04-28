#!/bin/bash

set -e

echo "📡 Starting Celery worker..."

# اجرای celery
exec celery -A src worker --loglevel=info

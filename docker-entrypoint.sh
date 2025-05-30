#!/bin/sh

# Exit on error
set -e

# Wait for database to be ready
echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Apply database migrations
echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..." # for production
# python manage.py collectstatic --noinput

# Create initial data
echo "Creating initial data..."
python manage.py load_books

# Start server
echo "Starting server..."
exec "$@"

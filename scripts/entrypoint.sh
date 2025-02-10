#!/bin/bash

# Wait for database to be ready
echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Run migrations
python manage.py migrate

# Create cache tables
python manage.py createcachetable

# Start command
exec "$@"
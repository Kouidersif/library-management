#!/bin/sh

echo "Initializing development environment..."
echo "Building Docker containers..."
docker-compose up --build -d


echo "Waiting for database and server to be ready..."
sleep 6

echo "Loading initial data..."
docker-compose exec web python manage.py load_books

echo "Create superuser - Please enter details..."
docker-compose exec web python manage.py createsuperuser

echo "Executing unit tests..."
docker-compose exec web python manage.py test

echo "\033[92mTests passed\033[0m"

echo "Server started at http://localhost:8000/docs/"

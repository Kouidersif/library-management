# Books Library

A Django-based Books Library Management System containerized with Docker.

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd books-library
   ```

2. Start the application:
   ```bash
   docker-compose up --build
   ```
   The application will be available at http://localhost:8000

3. Once you run the application, dummy books will be created for you otherwise run:
   ```bash
   docker-compose exec web python manage.py load_books
   ```

4. Create a superuser (in a new terminal): 
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

## Development with Docker

### Common Docker Commands

- Start the application:
  ```bash
  docker-compose up
  ```

- Start in detached mode:
  ```bash
  docker-compose up -d
  ```

- Stop the application:
  ```bash
  docker-compose down
  ```

- View logs:
  ```bash
  docker-compose logs -f
  ```

- Run migrations:
  ```bash
  docker-compose exec web python manage.py migrate
  ```

- Create superuser:
  ```bash
  docker-compose exec web python manage.py createsuperuser
  ```

- Run tests:
  ```bash
  docker-compose exec web python manage.py test
  ```

## API Endpoints

- `/admin/` - Django admin interface
- `/api/accounts/` - User account management
- `/api/books/` - Book management

## Features

- User App:
  - User Registration
  - User Login
  - User Token Refresh
  - User Logout
- Book App:
  - Books Listing
  - Book Details
  - Book Loaning
  - Book Return or End Loan
  - Admin Actions to end loans
  - Custom queryset managers for `Books` and `Loan` models to make queries easier


## Environment Variables

Create a `.env` file in the root directory with the following variables (for local development):

```
SECRET_KEY=changeme
DEBUG=True/False
POSTGRES_DB=db
POSTGRES_USER=changeme
POSTGRES_PASSWORD=changeme
DB_HOST=5432
```

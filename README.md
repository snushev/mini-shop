# MiniShop API

A **Django REST Framework (DRF)** application for managing a small-scale shop's inventory, customers, suppliers, purchases, and sales. The API provides user-specific data isolation, authentication via JWT, and comprehensive testing to ensure reliability.
Table of Contents

## Features

- Technologies
- Installation
- Usage
- API Endpoints
- Testing
- Authentication
- Contributing
- License

## Features

- User Authentication: Register and authenticate users using JSON Web Tokens (JWT).
- Data Isolation: Users can only access their own products, customers, suppliers, purchases, and sales.
- Inventory Management: Create, update, and delete products with category associations and stock tracking.
- Customer & Supplier Management: Manage customer and supplier details securely.
- Purchase & Sale Tracking: Record purchases from suppliers and sales to customers, with automatic stock updates.
- Filtering & Search: Advanced filtering, searching, and ordering capabilities for all endpoints.
- API Documentation: Interactive Swagger and ReDoc documentation for easy exploration of endpoints.

## Technologies

- Django 5.2.3: Web framework for rapid development and clean design.
- Django REST Framework: Toolkit for building Web APIs.
- Simple JWT: JSON Web Token authentication for secure user access.
- DRF-YASG: Swagger/OpenAPI documentation generator.
- Django Filters: Dynamic query filtering for API endpoints.
- Pytest: Testing framework for comprehensive unit and integration tests.
- Docker: Containerization platform
- Docker Compose: Multi-container orchestration
- PostgreSQL: Database container

## Installation

1. Clone the Repository

```bash
git clone https://github.com/yourusername/minishop-api.git
cd minishop-api
```

2. Set Up a Virtual Environment

- Create .env file (copy from .env.example)

- Configure your environment variables (DB credentials, SECRET_KEY, etc.)

3. Start with Docker

```bash
docker-compose up -d --build
```

4. Create Superuser (optional)

```bash
docker-compose exec web python manage.py createsuperuser
```

Access the API at `http://localhost:8000`.

## Docker Configuration

The project includes:

- `Dockerfile` for the Django application
- `docker-compose.yml` for the complete stack (Django + PostgreSQL)
- `.env.example` for environment variables template

Key containers:

- `web`: Django application
- `db`: PostgreSQL database

## Development with Docker

Common commands:

- Start containers: `docker-compose up -d`
- Stop containers: `docker-compose down`
- View logs: `docker-compose logs -f`
- Run tests: `docker-compose exec web pytest`
- Run management commands: `docker-compose exec web python manage.py [command]`

## Usage

1. Register a User

   - Send a `POST` request to `/register` with `username`, `email`, and `password`.
   - Receive `JWT` access and refresh tokens.

2. Authenticate

   - Obtain a token pair via `/api/token/` with `username` and `password`.
   - Include the access token in the `Authorization` header: `Bearer <access_token>`.

3. Explore the API

   - Visit `/swagger/` or `/redoc/` for interactive API documentation.
   - Use tools like Postman or cURL to interact with endpoints.

## API Endpoints

| Endpoint              | Methods          | Description                            |
| --------------------- | ---------------- | -------------------------------------- |
| `/register/`          | POST             | Register a new user                    |
| `/api/token/`         | POST             | Obtain JWT token pair                  |
| `/api/token/refresh/` | POST             | Refresh JWT access token               |
| `/categories/`        | GET, POST        | List or create categories              |
| `/categories/{id}/`   | GET, PUT, DELETE | Retrieve, update, or delete a category |
| `/products/`          | GET, POST        | List or create products                |
| `/products/{id}/`     | GET, PUT, DELETE | Retrieve, update, or delete a product  |
| `/customers/`         | GET, POST        | List or create customers               |
| `/customers/{id}/`    | GET, PUT, DELETE | Retrieve, update, or delete a customer |
| `/suppliers/`         | GET, POST        | List or create suppliers               |
| `/suppliers/{id}/`    | GET, PUT, DELETE | Retrieve, update, or delete a supplier |
| `/purchases/`         | GET, POST        | List or create purchases               |
| `/purchases/{id}/`    | GET, PUT, DELETE | Retrieve, update, or delete a purchase |
| `/sales/`             | GET, POST        | List or create sales                   |
| `/sales/{id}/`        | GET, PUT, DELETE | Retrieve, update, or delete a sale     |

## Filtering and Searching

- Most endpoints support filtering (e.g., `?name=Electronics`), searching (e.g., `?search=Laptop`), and ordering (e.g., `?ordering=price`).
- Refer to Swagger documentation for specific fields.

## Testing

The project includes comprehensive tests for all API endpoints using Pytest.

1. To run tests:

```bash
# Using Docker
docker-compose exec web pytest
```

```bash
# Or locally (with activated virtualenv)
pytest
```

2. Test Coverage

- Tests cover:

  - User-specific data isolation
  - CRUD operations for all models
  - Invalid data handling
  - Authentication and permission checks

- Example: `test_sale_api.py` verifies sale creation, stock updates, and access restrictions.

## Authentication

- JWT Authentication: All endpoints except /register/, `/swagger/`, and `/redoc/` require authentication.
- Permissions: The `IsOwner` permission ensures users can only access their own data.
- Token Management:
  - Obtain tokens via `/api/token/`.
  - Refresh tokens via `/api/token/refresh/`.

## Upcoming Features

The following features are planned to improve scalability, maintainability, and learning outcomes:

- Celery + Redis Integration
  Asynchronous task queue for handling background jobs such as sending confirmation emails, report generation, or long-running database operations.

- API Rate Limiting & Throttling
  Implement request throttling to protect the API from abuse and ensure fair usage.

- CI/CD with GitHub Actions
  Automate testing and deployment workflows using GitHub Actions for faster and safer delivery pipelines.

- Full-Text Search with PostgreSQL
  Enhance product search capabilities using PostgreSQL’s powerful full-text search.

- API Versioning
  Introduce versioning for the API to support future changes while maintaining backward compatibility.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

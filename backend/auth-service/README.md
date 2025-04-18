# Auth Service

The Authentication Service for the Learning Management System (LMS).

## Features

- User authentication with email/password
- OAuth2 support for social login
- JWT-based token authentication
- Password reset and account verification
- Role-based access control
- Multi-tenancy support (organization/branch)

## Technologies

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic for migrations
- JWT with python-jose
- Passlib with bcrypt

## Development Setup

### Prerequisites

- Python 3.11+
- PostgreSQL
- Redis (for token management and rate limiting)

### Local Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables (or create a `.env` file):
   ```
   ENVIRONMENT=development
   HOST=0.0.0.0
   PORT=8001
   SECRET_KEY=your_secret_key_for_development
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/lms_auth
   REDIS_URL=redis://localhost:6379/0
   ```

4. Run database migrations:
   ```
   alembic upgrade head
   ```

5. Start the service:
   ```
   uvicorn src.main:app --reload --port 8001
   ```

### Docker Setup

1. Build and start the service with Docker Compose:
   ```
   cd backend
   docker-compose up -d auth_service
   ```

## API Documentation

When the service is running, you can access:

- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## Available Endpoints

### Authentication

- `POST /api/auth/login` - Login with email and password
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/reset-password` - Request password reset
- `POST /api/auth/reset-password/confirm` - Confirm password reset
- `POST /api/auth/verify-email` - Verify email address
- `GET /api/auth/me` - Get current user profile

### OAuth2

- `POST /api/oauth/login` - Login with OAuth2 provider (Google, Facebook, GitHub, Apple)

## Testing

Run tests with pytest:

```
pytest
``` 
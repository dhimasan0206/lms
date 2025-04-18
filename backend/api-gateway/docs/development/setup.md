# Development Setup Guide

## Prerequisites

- Python 3.11 or higher
- Redis 6.0 or higher
- Docker and Docker Compose (optional)
- Git

## Local Development Setup

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd backend/api-gateway
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # For development dependencies
   ```

4. **Set Up Environment Variables**
   Create a `.env` file in the project root:
   ```env
   # Application
   APP_NAME=LMS API Gateway
   ENVIRONMENT=development
   DEBUG=true
   HOST=0.0.0.0
   PORT=8000

   # CORS
   CORS_ORIGINS=["http://localhost:3000"]

   # Service URLs
   AUTH_SERVICE_URL=http://localhost:8001
   USER_SERVICE_URL=http://localhost:8002
   COURSE_SERVICE_URL=http://localhost:8003
   CONTENT_SERVICE_URL=http://localhost:8004
   ENROLLMENT_SERVICE_URL=http://localhost:8005
   ASSESSMENT_SERVICE_URL=http://localhost:8006
   BADGE_SERVICE_URL=http://localhost:8007
   ANALYTICS_SERVICE_URL=http://localhost:8008
   NOTIFICATION_SERVICE_URL=http://localhost:8009

   # JWT
   JWT_SECRET_KEY=your-secret-key
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30

   # Redis
   REDIS_HOST=localhost
   REDIS_PORT=6379
   REDIS_DB=0

   # Logging
   LOG_LEVEL=DEBUG
   ```

5. **Start Redis**
   ```bash
   # Using Docker
   docker run -d --name redis -p 6379:6379 redis:6.0

   # Or install and start Redis locally
   # On macOS: brew install redis && brew services start redis
   # On Ubuntu: sudo apt-get install redis-server && sudo service redis start
   ```

6. **Run the Application**
   ```bash
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Docker Development Setup

1. **Build the Docker Image**
   ```bash
   docker build -t lms-api-gateway .
   ```

2. **Run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

## Development Tools

### Code Formatting
```bash
# Format code
black .

# Sort imports
isort .
```

### Linting
```bash
# Run linters
flake8
mypy .
```

### Testing
```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=src

# Run tests in watch mode
pytest-watch
```

### Documentation
```bash
# Generate OpenAPI documentation
python scripts/generate_openapi.py

# Serve documentation locally
python -m http.server 8001 -d docs
```

## Project Structure

```
api-gateway/
├── src/
│   ├── main.py              # Application entry point
│   ├── config/              # Configuration
│   │   ├── settings.py      # Settings management
│   │   └── constants.py     # Constants
│   ├── domain/              # Domain layer
│   │   ├── entities/        # Domain entities
│   │   ├── repositories/    # Repository interfaces
│   │   └── services/        # Domain services
│   ├── infrastructure/      # Infrastructure layer
│   │   ├── repositories/    # Repository implementations
│   │   └── services/        # External service integrations
│   └── interfaces/          # Interface layer
│       ├── api/             # API endpoints
│       │   ├── routes/      # Route definitions
│       │   └── models/      # API models
│       └── middlewares/     # Middleware components
├── tests/                   # Test suite
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── e2e/               # End-to-end tests
├── docs/                   # Documentation
├── scripts/               # Utility scripts
├── .env                   # Environment variables
├── .env.example          # Example environment variables
├── requirements.txt      # Production dependencies
├── requirements-dev.txt  # Development dependencies
└── README.md            # Project documentation
```

## Common Development Tasks

### Adding a New Endpoint

1. Create route handler in `src/interfaces/api/routes/`
2. Define request/response models in `src/interfaces/api/models/`
3. Implement business logic in `src/domain/services/`
4. Add tests in `tests/unit/` and `tests/integration/`
5. Update API documentation

### Adding a New Service Integration

1. Create service client in `src/infrastructure/services/`
2. Define service interface in `src/domain/services/`
3. Implement repository in `src/infrastructure/repositories/`
4. Add tests for the integration
5. Update service registry

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_service_registry.py

# Run tests with coverage
pytest --cov=src --cov-report=html

# Run tests in parallel
pytest -n auto
```

### Debugging

1. **Using VS Code**
   - Set breakpoints in the code
   - Press F5 to start debugging
   - Use the Debug Console for inspection

2. **Using PyCharm**
   - Set breakpoints in the code
   - Right-click and select "Debug"
   - Use the Debug tool window

3. **Using pdb**
   ```python
   import pdb; pdb.set_trace()
   ```

## Troubleshooting

### Common Issues

1. **Redis Connection Issues**
   - Check if Redis is running
   - Verify Redis connection settings in `.env`
   - Check Redis logs

2. **Service Registration Failures**
   - Verify service URLs in `.env`
   - Check service health endpoints
   - Review service registry logs

3. **Authentication Issues**
   - Verify JWT settings
   - Check token expiration
   - Review authentication logs

### Getting Help

1. Check the [troubleshooting guide](../operations/troubleshooting.md)
2. Review the [architecture documentation](../architecture/overview.md)
3. Consult the team's knowledge base
4. Reach out to the development team

## Best Practices

1. **Code Style**
   - Follow PEP 8 guidelines
   - Use type hints
   - Write docstrings
   - Keep functions small and focused

2. **Testing**
   - Write unit tests for all new code
   - Maintain high test coverage
   - Use meaningful test names
   - Follow AAA pattern (Arrange, Act, Assert)

3. **Documentation**
   - Keep documentation up to date
   - Document all public APIs
   - Include examples
   - Update changelog

4. **Version Control**
   - Use meaningful commit messages
   - Create feature branches
   - Keep commits small and focused
   - Review code before merging 
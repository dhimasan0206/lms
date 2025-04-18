# Course Service

A gRPC-based microservice for managing courses in the Learning Management System.

## Features

- Create, read, update, and delete courses
- Add and manage course content
- Stream course updates in real-time
- Filter and paginate course lists

## Architecture

This service follows Clean Architecture principles with distinct layers:

- **Domain Layer**: Core business logic and entities
- **Application Layer**: Use cases and business rules
- **Infrastructure Layer**: External concerns like database and messaging
- **Interface Layer**: API definitions and controllers

## Tech Stack

- **Language**: Python 3.11+
- **Framework**: gRPC
- **Database**: PostgreSQL with SQLAlchemy ORM
- **API**: Protocol Buffers
- **Containerization**: Docker

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Protocol Buffers compiler (for local development)

### Running with Docker Compose

The service is configured to run as part of the LMS backend:

```bash
# From the backend directory
docker-compose up -d course_service
```

### Local Development

1. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Run the service:

```bash
python -m src.main
```

### Testing with the Client

A test client is included to interact with the service:

```bash
# Create a new course
python client.py create_course

# Get a course by ID
python client.py get_course <course_id>

# List courses
python client.py list_courses
```

## API Documentation

The service API is defined in the `proto/course.proto` file. The main endpoints are:

- **CreateCourse**: Create a new course
- **GetCourse**: Get a course by ID
- **UpdateCourse**: Update an existing course
- **DeleteCourse**: Delete a course
- **ListCourses**: List courses with filtering and pagination
- **WatchCourse**: Stream updates to a course
- **AddCourseContent**: Add content to a course
- **GetCourseContent**: Get course content

## Database Schema

The service uses two main tables:

- **courses**: Stores course information and metadata
- **course_contents**: Stores course content items

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection URL (default: `postgresql+asyncpg://postgres:postgres@postgres:5432/lms_course`)
- `GRPC_PORT`: gRPC server port (default: `50051`)
- `GRPC_MAX_WORKERS`: Number of worker threads (default: `10`)
- `ENVIRONMENT`: Environment name (development, staging, production)
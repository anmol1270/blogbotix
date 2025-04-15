# AI Blog Assistant Backend

FastAPI backend for the AI Blog Assistant application that handles document processing, AI content generation, and WordPress integration.

## Features

- 🔐 JWT Authentication
- 📄 Document processing (PDF, Word)
- 🤖 AI-powered content generation using OpenAI
- 🎨 AI image generation
- 📝 WordPress integration
- 🗄️ PostgreSQL database
- 📚 OpenAPI documentation

## Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- OpenAI API
- Python-Jose (JWT)
- Alembic (Database migrations)
- Pytest (Testing)

## Prerequisites

- Python 3.8+
- PostgreSQL
- OpenAI API key
- WordPress site (optional)

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy the environment file and update the variables:
```bash
cp .env.example .env
```

4. Create the database:
```bash
createdb ai_blog_assistant
```

5. Run database migrations:
```bash
alembic upgrade head
```

## Running the Application

Start the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000
API documentation will be available at http://localhost:8000/docs

## API Endpoints

### Authentication
- POST /api/v1/auth/login - Login with Google OAuth
- POST /api/v1/auth/refresh - Refresh access token

### Users
- GET /api/v1/users/me - Get current user
- PUT /api/v1/users/me - Update current user

### Blog
- POST /api/v1/blog/upload - Upload document
- POST /api/v1/blog/generate - Generate blog post
- POST /api/v1/blog/publish - Publish to WordPress
- GET /api/v1/blog/posts - List blog posts

## Testing

Run tests:
```bash
pytest
```

## Project Structure

```
backend/
├── app/
│   ├── api/            # API endpoints
│   ├── core/           # Core configurations
│   ├── db/             # Database configuration
│   ├── models/         # SQLAlchemy models
│   ├── schemas/        # Pydantic models
│   ├── services/       # Business logic
│   └── utils/          # Utility functions
├── tests/              # Test files
├── alembic/            # Database migrations
├── requirements.txt    # Project dependencies
└── .env               # Environment variables
```

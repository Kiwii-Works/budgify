# Budgify API

FastAPI backend for Budgify application.

## Tech Stack

- **Framework**: FastAPI 0.115.0
- **Server**: Uvicorn
- **Database**: PostgreSQL
- **Migrations**: Alembic
- **Testing**: pytest
- **Linting**: ruff, black, mypy

## Setup

### Prerequisites

- Python 3.12.x
- PostgreSQL 14+
- Virtual environment tool

### Installation

1. Create and activate virtual environment:
```bash
cd apps/api
py -3.12 -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. Run migrations:
```bash
alembic upgrade head
```

### Running the Server

**Important**: Ejecuta el servidor desde el directorio `src/`:

```bash
# Navegar al directorio src
cd src

# Development mode with auto-reload
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# O usando la ruta relativa del venv desde src/
../.venv/Scripts/python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Alternativamente**, desde el directorio raíz `apps/api/`:

```bash
# Windows
set PYTHONPATH=src
.venv\Scripts\python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Linux/Mac
PYTHONPATH=src python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API documentation (Swagger UI): `http://localhost:8000/docs`

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest src/app/modules/health/tests/test_health.py -v
```

### Code Quality

```bash
# Lint check
ruff check src/

# Format check
black --check src/

# Type check
mypy src/

# Auto-fix linting issues
ruff check --fix src/

# Auto-format code
black src/
```

## Project Structure

```
apps/api/
├── src/
│   └── app/
│       ├── main.py              # FastAPI app entry point
│       ├── core/                # Core utilities (config, logging, db, errors)
│       ├── modules/             # Feature modules
│       │   ├── health/         # Health check endpoint
│       │   └── identity/       # Identity/auth module
│       └── tests/              # Shared test fixtures
├── alembic/                     # Database migrations
├── requirements.txt             # Python dependencies
├── pytest.ini                   # Pytest configuration
├── pyproject.toml              # Tool configuration
└── .env                        # Environment variables (not committed)
```

## Database Migrations

```bash
# Create new migration (autogenerate from models)
alembic revision --autogenerate -m "description"

# Apply all pending migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View current version
alembic current

# View migration history
alembic history
```

## API Endpoints

### Health Check
- `GET /api/health` - Basic health check

### Authentication (Phase 2+)
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh access token

## Environment Variables

See `.env.example` for all available configuration options.

Key variables:
- `DATABASE_URL`: PostgreSQL connection string
- `APP_ENV`: Environment (development, staging, production)
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `API_PREFIX`: API route prefix (default: /api)

## Clean Architecture

This project follows Clean Architecture principles:

- **api/**: HTTP routing only (FastAPI routers)
- **domain/**: Core business entities (plain Python, no framework deps)
- **application/**: Service layer, use cases
- **infrastructure/**: Concrete implementations (repositories, DB clients)
- **schemas/**: Pydantic DTOs for API boundary

## Contributing

1. Follow coding standards in `/docs/CODING_STANDARDS.md`
2. Write tests for new features
3. Ensure linting and type checks pass
4. Keep commits small and focused
5. Use conventional commit messages

## License

[Add license information]

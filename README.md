# Stock Predictor API

A FastAPI backend for stock price prediction using machine learning. Users can upload historical stock data, receive price predictions, analyze trends, and visualize historical performance.

---

## Features

- JWT authentication with bcrypt password hashing
- Upload historical stock data via CSV
- Stock price prediction using Linear Regression with moving averages (SMA_20, SMA_50)
- Historical trend analysis and data visualization
- User feedback system

---

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy 2.0, Pydantic v2
- **ML:** scikit-learn, pandas
- **Database:** PostgreSQL
- **Auth:** JWT (PyJWT), bcrypt
- **Migrations:** Alembic
- **Package manager:** uv
- **Containerization:** Docker, Docker Compose

---

## Project Structure

```
stock_predictor/
├── auth/               # JWT token generation and verification
├── config/             # App settings via pydantic-settings
├── database/           # SQLAlchemy engine, session, Base
├── dependencies/       # FastAPI dependencies (get_db, get_current_user)
├── feedback/           # Feedback domain (models, schemas, crud, service, router)
├── stock/              # Stock domain (models, schemas, crud, service, router)
└── user/               # User domain (models, schemas, crud, service, router)
main.py
alembic/
tests/
Dockerfile
docker-compose.yml
```

---

## Getting Started

### Prerequisites

- Docker and Docker Compose installed
- uv installed (`pip install uv`)

### Environment Variables

Create a `.env` file in the root directory based on `.env.example`:

```bash
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/stock_predictor
POSTGRES_USER=your-postgres-user
POSTGRES_PASSWORD=your-postgres-password
```

### Run with Docker

```bash
docker compose up --build
```

This will:
1. Start PostgreSQL and wait until healthy
2. Run Alembic migrations
3. Start the FastAPI server on `http://localhost:8000`

### Run locally

```bash
uv sync
alembic upgrade head
uv run main.py
```

---

## API Endpoints

### User

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/user/signup` | No | Register a new user |
| POST | `/user/login` | No | Login and receive JWT token |
| GET | `/user/profile` | Yes | Get current user profile |
| PUT | `/user/profile` | Yes | Update current user profile |

### Stock

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/stock/data` | Yes | Upload historical stock data (CSV) |
| GET | `/stock/predict` | Yes | Get price predictions |
| GET | `/stock/trends` | Yes | Get historical trend analysis |
| GET | `/stock/visualize` | Yes | Get data for visualization |

### Feedback

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/feedback` | Yes | Submit prediction feedback |

### Authentication

Protected endpoints require a Bearer token in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

### CSV Format

The stock data CSV must follow the OHLCV standard:

```csv
symbol,date_stamp,time_stamp,open,high,low,close,volume
AAPL,2024-01-01,14:30:00,185.50,186.20,184.90,185.80,52341000
```

---

## Running Tests

```bash
uv run pytest tests/
```

Tests use an in-memory SQLite database — no PostgreSQL required.

---

## Migrations

```bash
# Generate a new migration after model changes
alembic revision --autogenerate -m "description of change"

# Apply migrations
alembic upgrade head

# Revert last migration
alembic downgrade -1
```

---

## API Documentation

Interactive API docs available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
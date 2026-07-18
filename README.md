Here is the complete, professionally polished README.md in English for your GitHub portfolio:

Crypto Screener Backend
An asynchronous FastAPI backend application designed for tracking cryptocurrency exchange rates and managing investment portfolios. The project leverages background workers to periodically fetch live asset data from the CoinGecko API and stores historical and current price records in a PostgreSQL database.

🚀 Technology Stack
Framework: FastAPI (Python 3.11)

Database: PostgreSQL

ORM: SQLAlchemy (Asyncio / asyncpg)

Database Migrations: Alembic

Containerization: Docker / Docker Compose

Data Validation: Pydantic

🛠 Project Structure & Architecture
The project follows a clean, modular structure:

Plaintext
├── alembic/               # Database migration scripts managed by Alembic
├── src/                   # Main application source code
│   ├── routes/            # API endpoints (Routers)
│   │   ├── coins.py       # Manage the list of tracked crypto tokens
│   │   ├── exchange_rates.py # Fetch the latest exchange rates
│   │   ├── portfolio.py   # Investment portfolio metrics and logic
│   │   └── prices.py      # Historical token price tracking
│   ├── client.py          # Asynchronous external API client for CoinGecko
│   ├── config.py          # Application configuration and environment variable loading (.env)
│   ├── database.py        # SQLAlchemy engine setup and async session factories
│   ├── main.py            # Application entry point and lifespan state management
│   ├── models.py          # SQLAlchemy ORM database models (Coin, CoinPrice, ExchangeRate)
│   └── tasks.py           # Background workers and periodic cron tasks
├── .env                   # Local environment configuration file
├── alembic.ini            # Alembic configuration configuration
├── Dockerfile             # Multi-stage Docker build specification for the app
├── docker-compose.yml     # Container orchestration (FastAPI application + PostgreSQL)
└── requirements.txt       # Hardcoded python package dependencies list


⚡ Getting Started
1. Configure the Environment
Create a .env file in the root directory of the project and specify your database connection details (configured for the internal Docker network setup below):

DATABASE_URL= YOUR URL
2. Launch with Docker Compose
Build and run all services (FastAPI app and PostgreSQL instance) in detached mode with a single command:

Bash
docker-compose up -d --build
3. Run Database Migrations
Once the database container is healthy and accepting connections, apply your Alembic migrations to generate the schema:

Bash
alembic upgrade head
The server will be up and running at http://localhost:8001 (or http://localhost:8000 depending on your mapped compose ports).

Interactive API Documentation (Swagger UI): http://localhost:8001/docs

🔄 Automated Background Tasks
The application includes an active background worker that automatically manages state updates:

Queries the active token watchlists from the coins table.

Dispatches periodic requests to the external CoinGecko API for up-to-date USD valuations.

appends historical snapshots into the coin_prices table.

Updates current market rates inside the exchange_rates table securely using an atomic ON CONFLICT (...) DO UPDATE (Upsert) operation.
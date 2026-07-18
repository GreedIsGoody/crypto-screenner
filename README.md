# Crypto Screener & Portfolio Tracker

An asynchronous FastAPI backend application designed to track real-time cryptocurrency prices and calculate the profit/loss (PnL) of an investment portfolio. 

The application is architected as a pure, high-performance backend that utilizes asynchronous background workers to automatically fetch and update market rates in the database.

## 🚀 Key Features

*   **Crypto Screener:** Add and manage custom watchlists of target cryptocurrencies.
*   **Background Price Updates:** Background tasks periodically fetch and persist latest asset prices to a PostgreSQL database via external APIs.
*   **Transaction Ledger:** Track transactions with essential data points (ticker, transaction amount, purchase price in USD).
*   **Portfolio Analytics:** Calculate total portfolio cost, current market value, absolute profit/loss in USD, and percentage yield (PnL) on the fly.

---

## 🛠 Tech Stack

*   **Language:** Python 3.11+
*   **Framework:** FastAPI (Asynchronous)
*   **Database:** PostgreSQL
*   **ORM:** SQLAlchemy 2.0 (Async Engine & Session)
*   **Data Validation:** Pydantic v2
*   **Server:** Uvicorn with `uvloop` for high-throughput event looping

---

## 📂 Project Structure

```text
This  structure was made, just because a project is not too big, and we can contain logic in module architechture
crypto-screener/
├── src/
│   ├── routes/
│   │   ├── coins.py       # Endpoints for managing the watchlists
│   │   ├── prices.py      # Endpoints for retrieving asset prices
│   │   └── portfolio.py   # Transaction management and PnL calculation
│   ├── client.py          # API client for external crypto market data
│   ├── config.py          # Application settings & environment variables (.env)
│   ├── database.py        # SQLAlchemy async engine & session initialization
│   ├── main.py            # FastAPI application entry point
│   ├── models.py          # Declarative SQLAlchemy models (Coin, CoinPrice, Transaction)
│   └── tasks.py           # Background workers for regular price updates
├── .env                   # Local configuration file (ignored by Git)
├── .gitignore
├── Dockerfile
├── docker-compose.yml
└── requirements.txt

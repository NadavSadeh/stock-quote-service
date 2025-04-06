# Stock Quote Service

A backend Django-based microservice that provides stock exchange quotes using AlphaVantage API, with built-in caching and cost tracking.

## Features
- Fetches stock data via [AlphaVantage](https://www.alphavantage.co/)
- Smart caching based on trading hours & volatility
- Cost tracking for external API calls
- Logging with function-level decorator for observability
- Dockerized with Redis cache
- REST API endpoints
- Unit-tests

---
## Stack 
- Python 3.11+
- Django
- Redis (as cache backend)
- Docker & Docker Compose
- Gunicorn (production server)
- Unit tests via Django test client

---
## Getting Started


### 1. Clone the repository:

```bash
# Clone phase-1
git clone -b phase-1 https:/github.com/YOUR_USERNAME/stock-quote-service.git
cd stock-quote-service
```

___
### 2.  Environment Variables

Create a `.env` file in the **project root** (same directory as `docker-compose.yml`) and fill in your API key:
:
```example to .env file content
ALPHA_VANTAGE_API_KEY=your_api_key_here
USE_MOCK=0  # Set to "1" to use MockStockQuoteProvider
```
___
### 3. Build & run services:

```bash
docker-compose up --build
```

___
### 4. The app will be available at:

http://localhost:8000/

___
### 5. API Endpoints

| Method | URL                     | Description                          |
|--------|-------------------------|--------------------------------------|
| GET    | `/api/quote/<symbol>/` | Fetch quote for a given stock symbol |
| GET    | `/api/cost/`           | Get current accumulated API cost     |
| POST   | `/api/cost/reset/`     | Reset cost counter and cache         |


___
### 6. Run tests:

docker-compose exec web python manage.py test

___
### 7. Configuration:

Provider selection is controlled via the `USE_MOCK` environment variable.

In your `.env` file:

```env
USE_MOCK=1  # or 0
```
If USE_MOCK=1, the service will use the MockStockQuoteProvider, which returns static, predefined responses.
This is useful for local development and testing, as it avoids hitting the real AlphaVantage API.

If USE_MOCK=0, the service uses the real AlphaVantageProvider, making live API calls to fetch actual stock data.

This setting is loaded in settings.py and used dynamically at runtime to select the provider implementation.

Tip: Use mock mode when you're offline, testing repeatedly, or want consistent and fast responses.

___
### 8. Example Usage:

#### Get quote for a stock symbol
curl http://localhost:8000/api/quote/IBM/

#### Get total cost
curl http://localhost:8000/api/cost/

#### Reset cost and cache
curl -X POST http://localhost:8000/api/cost/reset/


___
### 9. Contact:

Built by Nadav Sadeh
For inquiries: nadavsa12@gmail.com

___






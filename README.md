# Stock Quote Service

A Django-based microservice that provides stock quotes from the AlphaVantage API, with smart caching, cost tracking, and IP-based rate limiting.

## Features
- Fetches stock data via [AlphaVantage](https://www.alphavantage.co/)
- Smart caching based on trading hours & volatility
- Cost tracking for external API calls
- Logging with function-level decorator for observability
- Dockerized with Redis cache
- REST API endpoints
- IP-based rate limiting for abuse prevention
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
# Clone phase-2 (with rate limiting and production-ready behavior)
git clone -b phase-2 https://github.com/NadavSadeh/stock-quote-service.git
cd stock-quote-service
```

___
### 2.  Environment Variables

Create a `.env` file in the **project root** (same directory as `docker-compose.yml`) and fill in your API key:
:
```bash
# .env file example
ALPHA_VANTAGE_API_KEY=your_api_key_here
USE_MOCK=0  # Set to "1" to use MockStockQuoteProvider
```
___
### 3. Build & run services:

```bash
docker-compose up --build
```

The app will be available at:

http://localhost:8000/

___
### 4. API Endpoints

| Method | URL                     | Description                          |
|--------|-------------------------|--------------------------------------|
| GET    | `/api/quote/<symbol>/` | Fetch quote for a given stock symbol |
| GET    | `/api/cost/`           | Get current accumulated API cost     |
| POST   | `/api/cost/reset/`     | Reset cost counter and cache         |


___
### 5. Example Usage:

#### Get quote for a stock symbol
curl http://localhost:8000/api/quote/IBM/

#### Get total cost
curl http://localhost:8000/api/cost/

#### Reset cost and cache
curl -X POST http://localhost:8000/api/cost/reset/

___
### 6. Stop services:

Stop services but keep Redis volume
```bash
docker-compose down
```
Stop services and delete Redis volume
```bash
docker-compose down -v
```

___
### 7. Rate Limiting (Phase 2):

To prevent abuse, the 'quote' endpoint is rate-limited to 10 requests per minute per IP.
If the limit is exceeded, the API returns 429 Too Many Requests response with the content of:
```
{
  "detail": "Request was throttled. Expected available in X seconds."
}
```
This is powered by Django REST Framework's built-in throttling, using the following setting in settings.py:

```
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'quote_ip': '10/min',
    }
}
```
___

### 8. Run tests:

docker-compose exec web python manage.py test

___
### 9. Configuration:

Provider selection is controlled via the `USE_MOCK` environment variable in your `.env` file:

```
USE_MOCK=1  # or 0
```
If USE_MOCK=1, the service will use the MockStockQuoteProvider, which returns static, predefined responses.
This is useful for local development and testing, as it avoids hitting the real AlphaVantage API.

If USE_MOCK=0, the service uses the real AlphaVantageProvider, making live API calls to fetch actual stock data.

This setting is loaded in settings.py and used dynamically at runtime to select the provider implementation.

Tip: Use mock mode when you're offline, testing repeatedly, or want consistent and fast responses.

___

### 10. Contact:

Author: Nadav Sadeh

___



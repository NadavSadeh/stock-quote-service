# Dockerfile
FROM python:3.13.2

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--timeout", "120", "stock_quote_service.wsgi:application", "--bind", "0.0.0.0:8000"]


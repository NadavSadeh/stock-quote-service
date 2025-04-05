import requests
from django.conf import settings
from .base import StockQuoteProvider, StockQuote



class AlphaVantageProvider(StockQuoteProvider):
    API_URL_TEMPLATE = (
        "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={apikey}"
    )
    def __init__(self):
        self.api_key = getattr(settings, "ALPHAVANTAGE_API_KEY", "YOUR_API_KEY")


    def get_quote(self, symbol):
        url = self.API_URL_TEMPLATE.format(symbol=symbol, apikey=self.api_key)
        raw = self.execute_and_validate("GET", url)

        if not raw:
            return None

        quote = raw.get("Global Quote", {})
        if "05. price" not in quote or "10. change percent" not in quote:
            return None

        return StockQuote(
            symbol=symbol,
            price=quote.get("05. price"),
            change_percent=quote.get("10. change percent"),
            raw_data=quote,
        )

    def execute_request(self, method, url, params=None, headers=None):
        return requests.request(method=method, url=url, params=params, headers=headers)

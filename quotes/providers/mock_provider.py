from .base import StockQuoteProvider, StockQuote
from quotes.logging_utils import log_function_call


#for dev only
class MockStockQuoteProvider(StockQuoteProvider):
    @log_function_call
    def get_quote(self, symbol):
        return StockQuote(
            symbol=symbol,
            price="123.45",
            change_percent="1.23%",
            raw_data={
                "03. high": "1.05",
                "04. low": "0.95",
                "05. price": "123.45",
                "10. change percent": "1.23%"
            }
        )

    def execute_request(self, *args, **kwargs):
        return None

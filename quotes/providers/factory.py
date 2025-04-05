from django.conf import settings
from .mock_provider import MockStockQuoteProvider
from .alphavantage import AlphaVantageProvider
from quotes.logging_utils import log_function_call


@log_function_call
def get_provider():
    use_mock = getattr(settings, "USE_MOCK_PROVIDER", "0")
    return MockStockQuoteProvider() if use_mock == "1" else AlphaVantageProvider()
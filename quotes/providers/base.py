from abc import ABC, abstractmethod
import logging
import requests
from quotes.logging_utils import log_function_call


logger = logging.getLogger(__name__)

class StockQuote:
    def __init__(self, symbol, price, change_percent, raw_data):
        self.symbol = symbol
        self.price = price
        self.change_percent = change_percent
        self.raw_data = raw_data

    def __repr__(self):
        return f"<StockQuote {self.symbol}: {self.price} ({self.change_percent})>"

class StockQuoteProvider(ABC):

    @abstractmethod
    def get_quote(self, symbol):
        pass

    @abstractmethod
    def execute_request(self, method, url, params=None, headers=None):
        """Must return a `requests.Response` object"""
        pass

    @log_function_call
    def execute_and_validate(self, method, url, **kwargs):
        try:
            response = self.execute_request(method, url, **kwargs)
            response.raise_for_status()

            data = response.json()
            if not data:
                logger.warning("Empty response received from API")
                return None

            return data
        except requests.RequestException as e:
            logger.error(f"Request error occurred: {e}")
        except ValueError as e:
            logger.error(f"Failed to parse JSON: {e}")
        return None

from django.core.cache import cache
from django.utils.timezone import now

from .constants import (
    COST_KEY,
    QUERY_COST,
    CACHE_KEY_TEMPLATE,
    TRADE_START_HOUR,
    TRADE_END_HOUR,
    CACHE_TIMEOUT_VOLATILE_PRICE,
    CACHE_TIMEOUT_STABLE_PRICE,
    CACHE_TIMEOUT_OFF_HOURS,
    VOLATILITY_THRESHOLD,
)

from .providers.factory import get_provider
from quotes.logging_utils import log_function_call


class StockQuoteService:
    def __init__(self):
        self.provider = get_provider()

    @staticmethod
    def is_trading_hours():
        current_hour = now().hour
        return TRADE_START_HOUR <= current_hour < TRADE_END_HOUR

    @log_function_call
    def get_cache_timeout(self, raw_data):
        try:
            high_price = float(raw_data.get("03. high", 0))
            low_price = float(raw_data.get("04. low", 0))
        except (ValueError, TypeError):
            return CACHE_TIMEOUT_OFF_HOURS

        if self.is_trading_hours():
            if high_price > VOLATILITY_THRESHOLD or low_price > VOLATILITY_THRESHOLD:
                return CACHE_TIMEOUT_VOLATILE_PRICE
            return CACHE_TIMEOUT_STABLE_PRICE

        return CACHE_TIMEOUT_OFF_HOURS

    @staticmethod
    def normalize_response(result):
        return {
            "symbol": result.symbol,
            "update_time": now().isoformat(),
            "price": result.price,
            "change_percent": result.change_percent,
        }
    @staticmethod
    def increment_cost():
        if cache.get(COST_KEY) is None:
            cache.set(COST_KEY, 0)
        cache.incr(COST_KEY, QUERY_COST)

    @log_function_call
    def get_stock_quote(self, symbol):
        cache_key = CACHE_KEY_TEMPLATE.format(symbol=symbol)
        cached = cache.get(cache_key)
        if cached:
            return cached

        result = self.provider.get_quote(symbol)
        if not result:
            return None

        response_data = self.normalize_response(result)
        timeout = self.get_cache_timeout(result.raw_data)

        cache.set(cache_key, response_data, timeout)
        self.increment_cost()
        return response_data


stock_quote_service_singleton = StockQuoteService()
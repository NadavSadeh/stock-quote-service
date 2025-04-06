from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache

from .service import stock_quote_service_singleton
from .constants import COST_KEY
from rest_framework.throttling import SimpleRateThrottle


class QuoteIPThrottle(SimpleRateThrottle):
    scope = 'quote_ip'

    def get_cache_key(self, request, view):
        return self.get_ident(request)


class StockQuoteView(APIView):
    throttle_classes = [QuoteIPThrottle]


    def get(self, request, symbol):
        service = stock_quote_service_singleton
        data = service.get_stock_quote(symbol)
        if not data:
            return Response({'error': 'Symbol not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data)


class TotalCostView(APIView):
    def get(self, request):
        value = cache.get(COST_KEY)
        cents = int(value) if value is not None else 0
        return Response({"total_cost": cents / 100})


class ResetCostView(APIView):
    def post(self, request):
        cache.set(COST_KEY, 0)
        keys = list(cache.iter_keys("stock_quote:*"))
        cache.delete_many(keys)
        return Response({"message": "Cost counter reset."})

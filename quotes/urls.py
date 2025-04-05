from django.urls import path

from .views import StockQuoteView, TotalCostView, ResetCostView

urlpatterns = [
    path('quote/<str:symbol>/', StockQuoteView.as_view(), name='quote'),
    path('cost/', TotalCostView.as_view(), name='get_cost'),
    path('cost/reset/', ResetCostView.as_view(), name='reset_cost'),
]

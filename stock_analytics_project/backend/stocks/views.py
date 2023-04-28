from rest_framework import generics
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import StockPrice, Stock, StockExchange, StockPortfolio
from .serializers import (
    StockPriceSerializer,
    SimpleStockSerializer,
    StockExchangeSerializer,
    StockPortfolioSerializer,
    HistoricalDataSerializer,
    AddStocktoPortfolioSerializer,
)
from .filters import StockPriceFilter

# Create your views here.


class ListStocks(generics.ListAPIView):
    serializer_class = SimpleStockSerializer
    queryset = Stock.objects.all()


class ListExchanges(generics.ListAPIView):
    serializer_class = StockExchangeSerializer
    queryset = StockExchange.objects.all()


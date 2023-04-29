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


class ListPortfolio(generics.ListAPIView):
    serializer_class = StockPortfolioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return StockPortfolio.objects.filter(owner=user)


class HistoricalData(generics.ListAPIView):
    queryset = StockPrice.objects.all()
    serializer_class = StockPriceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = StockPriceFilter

    def get_queryset(self):
        symbol = self.request.query_params.get("symbol")
        mic = self.request.query_params.get("mic")
        data = {"symbol": symbol, "mic": mic}
        
        serializer = HistoricalDataSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        symbol = serializer.validated_data["symbol"]
        mic = serializer.validated_data["mic"]
        
        queryset = StockPrice.objects.filter(
            stock__symbol=symbol, exchange__mic=mic
        ).select_related("stock", "exchange")
        return queryset


class AddStocktoPorfolioView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        context = {"owner": self.request.user}
        serializer = AddStocktoPortfolioSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

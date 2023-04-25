from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from .models import Stock, StockPrice, StockExchange, StockPortfolio


class StockPriceSerializer(serializers.ModelSerializer):
    stock = serializers.CharField()
    exchange = serializers.CharField()

    class Meta:
        model = StockPrice
        fields = [
            "stock",
            "exchange",
            "open",
            "close",
            "low",
            "high",
            "volume",
            "date",
        ]
        read_only = fields


class SimpleStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ["name", "symbol"]









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


class StockExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockExchange
        fields = ["name", "acronym", "mic", "country", "city", "website"]


class StockPortfolioSerializer(serializers.ModelSerializer):
    stocks = SimpleStockSerializer(many=True)

    class Meta:
        model = StockPortfolio
        fields = ["name", "owner", "stocks", "created_at", "updated_at"]


class HistoricalDataSerializer(serializers.Serializer):
    symbol = serializers.CharField(required=True)
    mic = serializers.CharField(required=True)

    def validate(self, attrs: dict) -> serializers.ValidationError | dict:
        symbol = attrs["symbol"]
        mic = attrs["mic"]

        try:
            Stock.objects.get(symbol=symbol, exchange__mic=mic)
        except Stock.DoesNotExist:
            raise serializers.ValidationError({"error": f"{symbol} is not registered on {mic}"})
        else:
            return attrs



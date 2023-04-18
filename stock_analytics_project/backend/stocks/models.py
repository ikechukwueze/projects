from django.db import models
from django.conf import settings

# Create your models here.


class StockExchange(models.Model):
    name = models.CharField(max_length=100)
    acronym = models.CharField(max_length=30, unique=True)
    mic = models.CharField(max_length=15, unique=True, db_index=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    website = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.acronym


class Stock(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10, unique=True, db_index=True)
    exchange = models.ManyToManyField(StockExchange, related_name="registered_stocks")

    def __str__(self) -> str:
        return self.symbol


class StockPortfolio(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    stocks = models.ManyToManyField(Stock)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StockPrice(models.Model):
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="stock_prices"
    )
    exchange = models.ForeignKey(
        StockExchange, on_delete=models.CASCADE, related_name="stock_prices"
    )
    open = models.FloatField(null=True)
    close = models.FloatField(null=True)
    low = models.FloatField(null=True)
    high = models.FloatField(null=True)
    volume = models.FloatField(null=True)
    adj_high = models.FloatField(null=True)
    adj_low = models.FloatField(null=True)
    adj_close = models.FloatField(null=True)
    adj_open = models.FloatField(null=True)
    adj_volume = models.FloatField(null=True)
    date = models.DateField()

    def __str__(self) -> str:
        return self.symbol

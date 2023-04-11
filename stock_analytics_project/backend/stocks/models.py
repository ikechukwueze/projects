from django.db import models
from django.conf import settings

# Create your models here.



class StockExchange(models.Model):
    name = models.CharField(max_length=100)
    acronym = models.CharField(max_length=30)
    mic = models.CharField(max_length=15)
    country = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    website = models.CharField(max_length=50)
    timezone = models.CharField(max_length=50)
    timezone_abbr = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.acronym


class Stock(models.Model):
    owners = models.ManyToManyField(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    exchange = models.ManyToManyField(StockExchange)

    def __str__(self) -> str:
        return self.symbol


class StockPrice(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    exchange = models.ForeignKey(StockExchange, on_delete=models.CASCADE)
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

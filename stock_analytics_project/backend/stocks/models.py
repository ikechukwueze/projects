from django.db import models

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


class Ticker(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    exchange = models.ManyToManyField(StockExchange)

    def __str__(self) -> str:
        return self.symbol


class StockPrice(models.Model):
    symbol = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    open = models.FloatField()
    close = models.FloatField()
    low = models.FloatField()
    high = models.FloatField()
    volume = models.FloatField()
    adj_high = models.FloatField()
    adj_low = models.FloatField()
    adj_close = models.FloatField()
    adj_open = models.FloatField()
    adj_volume = models.FloatField()
    date = models.DateTimeField()    

    def __str__(self) -> str:
        return self.symbol

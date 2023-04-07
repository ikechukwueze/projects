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




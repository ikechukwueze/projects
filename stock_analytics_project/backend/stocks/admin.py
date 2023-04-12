from django.contrib import admin
from .models import StockExchange, StockPrice, Stock

# Register your models here.


class StockExchangeAdmin(admin.ModelAdmin):
    list_display = ["name", "acronym"]
    search_fields = ["name", "acronym"]


class StockPriceAdmin(admin.ModelAdmin):
    list_display = ["stock", "open", "close", "high", "low", "volume"]
    search_fields = ["symbol"]


class StockAdmin(admin.ModelAdmin):
    list_display = ["name", "symbol"]
    search_fields = ["name", "symbol"]
    list_filter = ["exchange"]




admin.site.register(StockExchange, StockExchangeAdmin)
admin.site.register(StockPrice, StockPriceAdmin)
admin.site.register(Stock, StockAdmin)
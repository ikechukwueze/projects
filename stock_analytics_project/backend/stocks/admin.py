from datetime import datetime
from django.contrib import admin
from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
from .models import StockExchange, StockPrice, Stock, StockPortfolio

# Register your models here.


class StockExchangeAdmin(admin.ModelAdmin):
    list_display = ["name", "acronym"]
    search_fields = ["name", "acronym"]


class StockPriceResource(resources.ModelResource):
    stock = Field(
        column_name="Stock",
        attribute="stock",
        widget=ForeignKeyWidget(Stock, field="symbol"),
    )
    exchange = Field(
        column_name="Exchange",
        attribute="exchange",
        widget=ForeignKeyWidget(StockExchange, field="acronym"),
    )
    date = Field(attribute="date", column_name="Date")
    open_ = Field(attribute="open", column_name="Open")
    high = Field(attribute="high", column_name="High")
    low = Field(attribute="low", column_name="Low")
    close = Field(attribute="close", column_name="Close/Last")
    volume = Field(attribute="volume", column_name="Volume")

    class Meta:
        model = StockPrice
        fields = [
            "stock",
            "exchange",
            "date",
            "open_",
            "high",
            "low",
            "close",
            "volume",
        ]
        import_id_fields = ["stock", "exchange", "date"]

    def before_import_row(self, row, row_number=None, **kwargs):
        # modify row
        date_str = row["Date"]
        old_format = "%d/%m/%Y"
        new_format = "%Y-%m-%d"

        row["Date"] = datetime.strptime(date_str, old_format).strftime(new_format)
        row["Close/Last"] = row["Close/Last"].replace("$", "")
        row["Open"] = row["Open"].replace("$", "")
        row["High"] = row["High"].replace("$", "")
        row["Low"] = row["Low"].replace("$", "")


class StockPriceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = StockPriceResource

    list_display = ["stock", "exchange", "open", "close", "high", "low", "volume", "date"]
    search_fields = ["symbol"]
    list_filter = ["stock__symbol"]
    list_select_related = ["stock"]


class StockAdmin(admin.ModelAdmin):
    list_display = ["name", "symbol"]
    search_fields = ["name", "symbol"]
    list_filter = ["exchange"]


class StockPortfolioAdmin(admin.ModelAdmin):
    list_display = ["owner", "name", "created_at"]
    search_fields = ["owner__username", "stocks__symbol"]


admin.site.register(StockExchange, StockExchangeAdmin)
admin.site.register(StockPrice, StockPriceAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(StockPortfolio, StockPortfolioAdmin)

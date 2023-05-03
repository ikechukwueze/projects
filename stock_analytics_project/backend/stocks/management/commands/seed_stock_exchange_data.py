from django.core.management.base import BaseCommand
from django.db import transaction
import requests
import os
import json
from decouple import config
from stocks.models import StockExchange, Stock



BASE_URL = config("MARKET_STACK_BASE_URL")
API_KEY = config("MARKET_STACK_API_KEY")


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         "--exchange", type=str, help="Stock exchange to retrieve stocks"
    #     )

    # def handle(self, *args, **options):
    #     mic = options["exchange"]
    #     url = f"{BASE_URL}/exchanges/{mic}/tickers?access_key={API_KEY}&limit=1000"
        
    #     try:
    #         response = requests.get(url)
    #         response.raise_for_status()
    #     except requests.exceptions.HTTPError as err:
    #         raise err
    #     else:
    #         response_data = response.json()
    #         data = response_data["data"]
    #         return data


    def handle(self, *args, **options):
        file_path = os.path.join(os.path.dirname(__file__), "nasdaq_stocks.json")
        bulk_stocks = []
        
        with open(file_path) as f:
           json_file = json.load(f)
           data = json_file["data"]
           tickers = data.pop("tickers")
           exchange = StockExchange.objects.create(**data)
           
           for ticker in tickers:
                ticker.pop("has_intraday")
                ticker.pop("has_eod")
                try:
                    stock = Stock.objects.create(**ticker)
                except:
                    pass
                else:
                    exchange.registered_stocks.add(stock)
        
        print("done")

           



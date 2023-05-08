from datetime import date
from datetime import timedelta
from datetime import datetime
from decouple import config
import requests
from django.db import transaction
from .models import StockExchange, Stock, StockPrice, StockPortfolio


BASE_URL = config("MARKET_STACK_BASE_URL")
API_KEY = config("MARKET_STACK_API_KEY")


def modify_date(input_date: str | None) -> str:
    today = date.today()
    yesteday = today - timedelta(days=1)
    one_year_ago = today - timedelta(days=360)
    date_format = "%Y-%m-%d"

    if input_date is None:
        return one_year_ago.strftime(date_format)

    date_obj = datetime.strptime(input_date, date_format).date()

    if date_obj >= today:
        return yesteday.strftime(date_format)

    if date_obj < one_year_ago:
        return one_year_ago.strftime(date_format)

    return input_date


def retrieve_eod_stock_price_data(
    symbol: str, mic: str, date_from: str = None
) -> list[dict] | Exception:
    # future modification,
    # ticker should be list of tickers
    limit = 1000
    date = modify_date(date_from)
    url = f"{BASE_URL}/eod?access_key={API_KEY}&exchange={mic}&symbols={symbol}&limit={limit}&date_from={date}"

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise err
    else:
        response_data = response.json()
        data = response_data["data"]
        return data


def save_eod_stock_price_data(eod_stock_price_data: list[dict]) -> None:
    for data in eod_stock_price_data:
        symbol = data.pop("symbol")
        mic = data.pop("exchange")
        date = data.pop("date").split("T")[0]

        stock = Stock.objects.get(symbol=symbol)
        exchange = StockExchange.objects.get(mic=mic)
        params = {}

        for key, value in data.items():
            if hasattr(StockPrice(), key):
                params[key] = value

        _, created = StockPrice.objects.get_or_create(
            stock=stock, exchange=exchange, date=date, defaults=params
        )


@transaction.atomic
def add_new_stock_to_portfolio(
    owner, symbol: str, mic: str, portfolio_name: str, date_from: str = None
) -> None:
    
    stock = Stock.objects.get(symbol=symbol, exchange__mic=mic)
    portfolio = StockPortfolio.objects.get(owner=owner, name=portfolio_name)
    portfolio.stocks.add(stock)
    
    eod_stock_price_data = retrieve_eod_stock_price_data(symbol, mic, date_from)
    save_eod_stock_price_data(eod_stock_price_data)
from django.test import TestCase
from django.contrib.auth import get_user_model
from stocks.helpers import (
    modify_date,
    retrieve_eod_stock_price_data,
    save_eod_stock_price_data,
    add_new_stock_to_portfolio,
)
from unittest.mock import patch
from datetime import date, timedelta
from unittest import mock
import json
from requests.exceptions import HTTPError
from .fake_response import (
    FakeJsonResponse,
    mock_400_bad_request,
    mock_successful_eod_stock_request,
)
import os
from stocks.models import StockPrice, StockPortfolio


class TestHelperFunction(TestCase):
    fixtures = ["stocks.json", "stock_exchange.json"]

    def setUp(self) -> None:
        self.symbol = "AAPL"
        self.exchange = "XNAS"
        self.user_model = get_user_model()
        json_file = os.path.join(os.path.dirname(__file__), "apple_stock_prices.json")
        with open(json_file) as f:
            self.apple_eod_data = json.load(f)["data"]

    def test_modify_date(self):
        date_format = "%Y-%m-%d"
        today = date.today()
        current_date = today.strftime(date_format)
        yesteday = (today - timedelta(days=1)).strftime(date_format)
        one_year_ago = (today - timedelta(days=360)).strftime(date_format)
        future_date = (today + timedelta(days=4)).strftime(date_format)
        past_date = (today - timedelta(days=365)).strftime(date_format)

        self.assertEqual(modify_date(current_date), yesteday)
        self.assertEqual(modify_date(yesteday), yesteday)
        self.assertEqual(modify_date(future_date), yesteday)
        self.assertEqual(modify_date(past_date), one_year_ago)
        self.assertEqual(modify_date(one_year_ago), one_year_ago)
        self.assertEqual(modify_date(None), one_year_ago)

    @mock.patch("requests.get", side_effect=mock_successful_eod_stock_request)
    def test_retrieve_eod_stock_price_data(self, mock_get):
        response = retrieve_eod_stock_price_data(self.symbol, self.exchange)
        self.assertIsInstance(response, list)
        self.assertEqual(response, self.apple_eod_data)

    @mock.patch("requests.get", side_effect=mock_400_bad_request)
    def test_retrieve_eod_stock_price_data_raises_httperror_for_unsuccessful_request(
        self, mock_get
    ):
        with self.assertRaises(HTTPError):
            retrieve_eod_stock_price_data(self.symbol, self.exchange)

    def test_save_eod_stock_price_data(self):
        save_eod_stock_price_data(self.apple_eod_data)
        self.assertEqual(StockPrice.objects.count(), len(self.apple_eod_data))

    @mock.patch("requests.get", side_effect=mock_successful_eod_stock_request)
    def test_add_new_stock_to_porfolio(self, mock_get):
        owner = self.user_model.objects.create(
            username="john", email="jlennon@beatles.com", password="glass_onion"
        )
        add_new_stock_to_portfolio(owner, self.symbol, self.exchange)
        self.assertEqual(StockPrice.objects.count(), len(self.apple_eod_data))
        self.assertEqual(StockPortfolio.objects.count(), 1)
        self.assertEqual(StockPortfolio.objects.first().owner, owner)
        self.assertEqual(StockPortfolio.objects.first().stock.symbol, self.symbol)
        self.assertEqual(StockPortfolio.objects.first().exchange.mic, self.exchange)

    # def test_extract_finding_data(self):
    #     result = self.data["results"][0]
    #     return_val = extract_finding_data(
    #         result
    #     )  # target_id, definition_id, url, path, method, scans
    #     self.assertIsInstance(return_val, tuple)
    #     self.assertEqual(return_val[0], result["target"]["id"])
    #     self.assertEqual(return_val[1], result["definition"]["id"])
    #     self.assertEqual(return_val[2], result["url"])
    #     self.assertEqual(return_val[3], result["path"])
    #     self.assertEqual(return_val[4], result["method"])
    #     self.assertEqual(return_val[5], result["scans"])

    # def test_saving_finding_data(self):
    #     result = self.data["results"][0]
    #     target_id = result["target"]["id"]
    #     definition_id = result["definition"]["id"]
    #     url = result["url"]
    #     path = result["path"]
    #     method = result["method"]
    #     scans = result["scans"]

    #     save_finding_data(target_id, definition_id, url, path, method, scans)

    #     self.assertEqual(Finding.objects.count(), 1)
    #     self.assertEqual(Finding.objects.first().target_id, target_id)

    #     scan_list = list(Scan.objects.all().values_list("scan", flat=True))
    #     self.assertEqual(Scan.objects.count(), len(scans))
    #     self.assertTrue(Scan.objects.filter(finding__target_id=target_id).exists())
    #     self.assertEqual(Scan.objects.values("finding_id").distinct().count(), 1)
    #     self.assertEqual(scans, scan_list)

    # @mock.patch("requests.get", side_effect=mocked_get_request)
    # def test_process_finding_response(self, mock_get):
    #     json_file = os.path.join(os.path.dirname(__file__), "fake_response_page_1.json")
    #     with open(json_file) as f:
    #         data = json.load(f)

    #     count = data["count"]
    #     self.assertEqual(Finding.objects.count(), 0)
    #     process_finding_response(self.base_findings_url, self.headers)
    #     self.assertEqual(Finding.objects.count(), count)

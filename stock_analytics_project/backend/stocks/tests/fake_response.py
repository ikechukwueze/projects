import os
import json
from requests.exceptions import HTTPError


class FakeJsonResponse(object):
    status_code = 200
    response_files = {"apple_stocks": "apple_stock_prices.json"}
    file_name = None

    def json(self):
        json_file = os.path.join(
            os.path.dirname(__file__), self.response_files[self.file_name]
        )
        with open(json_file) as f:
            f = json.load(f)
        return f

    def raise_for_status(self):
        if not str(self.status_code).startswith("2"):
            raise HTTPError


def mocked_get_request(*args, **kwargs):
    fake_response = FakeJsonResponse()
    return fake_response


def mock_400_bad_request(*args, **kwargs):
    fake_response = FakeJsonResponse()
    fake_response.status_code = 400
    return fake_response


def mock_successful_eod_stock_request(*args, **kwargs):
    fake_response = FakeJsonResponse()
    fake_response.file_name = "apple_stocks"
    return fake_response
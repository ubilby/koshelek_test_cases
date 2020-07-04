from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from sys import getsizeof
import json
import time
import datetime

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'  # pro_api
# url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'  # sandbox api

parameters = {
    "start": "0",
    "limit": "10",
    "convert": "USD",
    "sort": "volume_24h"
}

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '08d4e9ad-9b13-4dd9-83fd-7eee09d1ca61',  # pro_api
  # 'X-CMC_PRO_API_KEY': '9adea28d-5568-4eb3-870b-e3b943036e35',  # sand_box_api
}

session = Session()
session.headers.update(headers)
# connet and check the time for answer
time_request = time.time()

try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    # print(data)

except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

time_response = time.time()

# check what dates are actually
today = datetime.datetime.isoformat(datetime.datetime.utcnow(), sep='T')[:10]
dates_are_actually = True
not_actually_tickers = []
for i in data["data"]:
    if i["last_updated"][:10] != today:
        dates_are_actually = False
        not_actually_tickers.append(i["name"])


# asserts
assert data["status"]["error_code"] == 0, data["status"]["error_message"]
assert time_response - time_request < 0.5, "time period is longer than 500ms"
assert getsizeof(response.text) < 10240, "response is too large"
assert dates_are_actually, "This tickers dates are not actually: " + " ".join(not_actually_tickers)

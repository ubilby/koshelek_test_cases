import aiohttp
import asyncio
import time
import json
import datetime
from statistics import quantiles


parameters = {
    "start": "1",
    "limit": "10",
    "convert": "USD",
    "sort": "volume_24h"
}

headers_sandbox = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '9adea28d-5568-4eb3-870b-e3b943036e35',  # sand_box_api
}

headers_pro = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '08d4e9ad-9b13-4dd9-83fd-7eee09d1ca61',  # pro_api
}

url_pro = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'  # pro_api
url_sandbox = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'  # sandbox api
answers_times = []


async def main(url):
    async with aiohttp.ClientSession(headers=headers_pro) as session:
        start = time.time()
        async with session.get(url, params=parameters) as response:
            answer = await response.text()
            end = time.time()

            assert end - start < 0.5, "latency is 500ms or more"
            answers_times.append(end - start)

            data = json.loads(answer)
            assert data["status"]["error_code"] == 0, data["status"]["error_message"]

            today = datetime.datetime.isoformat(datetime.datetime.utcnow(), sep='T')[:10]
            dates_are_actually = True

            for i in data["data"]:

                if i["last_updated"][:10] != today:
                    dates_are_actually = False

            assert dates_are_actually, "Ticker's dates are not actually!"

            response_size = len(answer)
            assert response_size < 10240, "Response is too large"

            return answer


loop = asyncio.get_event_loop()
coroutines = [main(url_pro) for _ in range(8)]
results = loop.run_until_complete(asyncio.gather(*coroutines))
timestamps = [datetime.datetime.strptime(json.loads(i)['status']['timestamp'][:-1],
    '%Y-%m-%dT%H:%M:%S.%f').timestamp() for i in results]

rps = len(timestamps)/(max(timestamps) - min(timestamps))
assert rps > 5, "rps isn't more than 5"

latency_80_percentil = quantiles(answers_times, n=100, method="inclusive")[80]
assert latency_80_percentil < 0.45, "80% lanetcy >= 0.45"

print("""Everything passed:
    - Packages sizes are less than 10KB
    - Information is relevant
    - Latency < 0.5s
    - 80% lanetcy < 0.45s
    - rps > 5""")

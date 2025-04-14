import requests

class ExchangeRateToolkit:
    def __init__(self):
        self.api_key = "381bfbd47d134bea88f30a7d5606ef4f"
        self.supported_pairs = [("USD", "INR"), ("EUR", "INR"), ("JPY", "INR"), ("CHF", "INR")]

    def get_exchange_rates(self) -> str:
        responses = []
        for base, target in self.supported_pairs:
            url = f"https://api.twelvedata.com/exchange_rate?symbol={base}/{target}&apikey={self.api_key}"
            r = requests.get(url)
            data = r.json()
            if 'rate' in data:
                rate = float(data['rate'])
                responses.append(f"**{base}/{target}** = `{rate}`")
            else:
                responses.append(f"Error fetching {base}/{target}: {data.get('message', 'Unknown error')}")
        return "\n".join(responses)

# Instantiate and use the toolkit
exchange_rate_toolkit = ExchangeRateToolkit()
exchange_rates = exchange_rate_toolkit.get_exchange_rates()
print(exchange_rates)

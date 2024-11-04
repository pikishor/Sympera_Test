import requests
import logging

class ExchangeRate:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_exchange_rate(self, from_currency, to_currency='USD'):
        """
        Fetches the exchange rate from one currency to another.

        Parameters:
            from_currency (str): The currency code to convert from (e.g., 'EUR').
            to_currency (str): The currency code to convert to (default is 'USD').

        Returns:
            float: The exchange rate if successful, otherwise None.
        """
        try:
            url = f"https://api.frankfurter.app/latest?from={from_currency}&to={to_currency}"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()['rates'][to_currency]
            else:
                print("Error fetching exchange rate.")
                return None
        except Exception as e:
            self.logger.error(f"Error fetching exchange rate: {e}")
            raise
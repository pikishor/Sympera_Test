import unittest
from unittest.mock import patch, MagicMock
import logging
from src.utils.exchange_rate_utils import ExchangeRate  # Adjust the import based on your module structure

class TestExchangeRate(unittest.TestCase):

    @patch('requests.get')
    def test_get_exchange_rate_success(self, mock_get):
        # Mock a successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'rates': {
                'USD': 1.2
            }
        }
        mock_get.return_value = mock_response

        exchange_rate = ExchangeRate()
        result = exchange_rate.get_exchange_rate('EUR', 'USD')

        # Assertions
        self.assertEqual(result, 1.2)
        mock_get.assert_called_once_with("https://api.frankfurter.app/latest?from=EUR&to=USD")

    @patch('requests.get')
    def test_get_exchange_rate_failure_status_code(self, mock_get):
        # Mock an API response with a failure status code
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_get.return_value = mock_response

        exchange_rate = ExchangeRate()
        result = exchange_rate.get_exchange_rate('EUR', 'USD')

        # Assertions
        self.assertIsNone(result)
        mock_get.assert_called_once_with("https://api.frankfurter.app/latest?from=EUR&to=USD")

    @patch('requests.get')
    def test_get_exchange_rate_exception(self, mock_get):
        # Mock an exception being raised during the request
        mock_get.side_effect = Exception("Network error")

        exchange_rate = ExchangeRate()

        with self.assertRaises(Exception) as context:
            exchange_rate.get_exchange_rate('EUR', 'USD')

        # Assertions
        self.assertEqual(str(context.exception), "Network error")
        mock_get.assert_called_once_with("https://api.frankfurter.app/latest?from=EUR&to=USD")

if __name__ == '__main__':
    unittest.main()

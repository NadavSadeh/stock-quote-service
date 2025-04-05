from unittest import TestCase
from unittest.mock import patch, Mock
from quotes.providers.alphavantage import AlphaVantageProvider


class AlphaVantageProviderErrorHandlingTests(TestCase):

    @patch("quotes.providers.alphavantage.AlphaVantageProvider.execute_request")
    def test_returns_none_on_bad_status_code(self, mock_request):
        mock_response = Mock(status_code=500)
        mock_response.json.return_value = {}
        mock_request.return_value = mock_response

        provider = AlphaVantageProvider()
        result = provider.get_quote("IBM")
        self.assertIsNone(result)

    @patch("quotes.providers.alphavantage.AlphaVantageProvider.execute_request")
    def test_returns_none_on_exception(self, mock_request):
        import requests
        mock_request.side_effect = requests.RequestException("fail")

        provider = AlphaVantageProvider()
        result = provider.get_quote("IBM")
        self.assertIsNone(result)

    @patch("quotes.providers.alphavantage.AlphaVantageProvider.execute_request")
    def test_returns_none_on_missing_global_quote(self, mock_request):
        mock_response = Mock(status_code=200)
        mock_response.json.return_value = {}
        mock_request.return_value = mock_response

        provider = AlphaVantageProvider()
        result = provider.get_quote("IBM")
        self.assertIsNone(result)

    @patch("quotes.providers.alphavantage.AlphaVantageProvider.execute_request")
    def test_successful_quote_parsing(self, mock_request):
        mock_response = Mock(status_code=200)
        mock_response.json.return_value = {
            "Global Quote": {
                "05. price": "123.45",
                "10. change percent": "0.50%"
            }
        }
        mock_request.return_value = mock_response

        provider = AlphaVantageProvider()
        result = provider.get_quote("IBM")

        self.assertIsNotNone(result)
        self.assertEqual(result.symbol, "IBM")
        self.assertEqual(result.price, "123.45")
        self.assertEqual(result.change_percent, "0.50%")

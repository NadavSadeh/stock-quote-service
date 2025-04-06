from django.test import TestCase
from rest_framework.test import APIClient
from django.core.cache import cache


class QuoteThrottlingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        cache.clear()

    def tearDown(self):
        cache.clear()

    def test_quote_endpoint_throttles_after_10_requests_per_ip(self):
        url = "/api/quote/IBM/"
        for i in range(10):
            res = self.client.get(url)
            self.assertIn(res.status_code, [200, 404], f"Failed on request #{i+1}")

        # 11th request - should be throttled
        res = self.client.get(url)
        self.assertEqual(res.status_code, 429)
        self.assertIn("detail", res.json())
        self.assertIn("throttled", res.json()["detail"].lower())
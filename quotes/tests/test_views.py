from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache

from quotes.constants import COST_KEY, QUERY_COST


class QuoteServiceTests(TestCase):
    def setUp(self):
        cache.clear()

    def tearDown(self):
        cache.clear()

    def test_quote_response_structure(self):
        response = self.client.get(reverse('quote', args=['IBM']))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("symbol", data)
        self.assertIn("update_time", data)
        self.assertIn("price", data)
        self.assertIn("change_percent", data)

    def test_cost_increases_after_query(self):
        self.client.get(reverse('quote', args=['IBM']))
        cost = cache.get(COST_KEY)
        self.assertEqual(cost, QUERY_COST)

    def test_cost_does_not_increase_from_cache(self):
        self.client.get(reverse('quote', args=['IBM']))  # First request triggers cost
        cost_first = cache.get(COST_KEY)
        self.client.get(reverse('quote', args=['IBM']))  # Should hit cache
        cost_second = cache.get(COST_KEY)
        self.assertEqual(cost_first, cost_second)

    def test_cost_reset_successfully(self):
        self.client.get(reverse('quote', args=['IBM']))
        response = self.client.post(reverse('reset_cost'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(cache.get(COST_KEY), 0)
        self.assertIsNone(cache.get("stock_quote:IBM"))

    def test_get_total_cost_endpoint(self):
        self.client.get(reverse('quote', args=['IBM']))
        response = self.client.get(reverse('get_cost'))
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertIn("total_cost", json)
        self.assertEqual(json["total_cost"], QUERY_COST / 100)

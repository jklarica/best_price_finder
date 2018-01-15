from __future__ import unicode_literals
from datetime import date
from decimal import Decimal

from django.test import TestCase

from products.models import Product, PricingBlock
from products.utils import get_price, get_lowest_price_blocks


class TestUtils(TestCase):
    def setUp(self):
        Product(id=1, name='Test Product', published=True, currency='GBP').save()
        PricingBlock(id=1, start_date='2020-01-01', end_date='2020-01-08', nights=7, price=700.00, product_id=1).save()
        PricingBlock(id=2, start_date='2020-01-08', end_date='2020-01-15', nights=1, price=100.00, product_id=1).save()
        PricingBlock(id=3, start_date='2020-01-08', end_date='2020-01-16', nights=1, price=120.00, product_id=1).save()
        PricingBlock(id=4, start_date='2020-01-08', end_date='2020-01-16', nights=1, price=150.00, product_id=1).save()
        PricingBlock(id=5, start_date='2020-01-08', end_date='2020-01-16', nights=1, price=180.00, product_id=1).save()
        PricingBlock(id=6, start_date='2020-01-05', end_date='2020-01-08', nights=3, price=250.00, product_id=1).save()
        PricingBlock(id=7, start_date='2020-01-10', end_date='2020-01-16', nights=2, price=150.00, product_id=1).save()

    def test_find_best_price(self):
        first_stay = get_price(
            Product.objects.get(id=1),
            date(2020, 1, 1),
            15
        )

        second_stay = get_price(
            Product.objects.get(id=1),
            date(2020, 1, 8),
            6
        )

        self.assertEqual(first_stay['price'], Decimal('1350'))
        self.assertEqual(
            [1, 2, 2, 7, 7, 7],
            [block.id for block in first_stay['blocks']]
        )

        self.assertEqual(second_stay['price'], Decimal('500'))
        self.assertEqual(
            [2, 2, 7, 7],
            [block.id for block in second_stay['blocks']]
        )

    def test_reduce_pricing_blocks(self):
        blocks = get_lowest_price_blocks(1)
        self.assertEqual(
            [1, 2, 3, 6, 7],
            [block.id for block in blocks]
        )

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date
from decimal import Decimal

from django.test import TestCase

from products.utils import get_price
from products.models import Product


class TestUtils(TestCase):
    def test_find(self):
        best_price = get_price(
            Product.objects.get(id=1),
            date(2020, 1, 1),
            15
        )

        self.assertEqual(best_price['price'], Decimal('1350'))
        self.assertEqual(
            [1, 2, 2, 7, 7, 7],
            [block.id for block in best_price['blocks']]
        )

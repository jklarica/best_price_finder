# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    published = models.BooleanField(default=False)
    currency = models.CharField(max_length=3)

    def __unicode__(self):
        return self.name


class PricingBlock(models.Model):
    """
    A period of time that a 'product' can be booked.

    The block can be booked between 'start_date' and 'end_date' for the number
    of days specified, where the 'end_date' is not inclusive.

    For example, a 1 night block between 2016-01-01 and 2016-01-04 can be
    booked on the 1st, 2nd or 3rd for a night.

    The 'price' is the total for the number of nights.
    """
    id = models.IntegerField(primary_key=True)
    product = models.ForeignKey(Product)
    start_date = models.DateField()
    end_date = models.DateField()
    nights = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

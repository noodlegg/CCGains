"""Models, as Model in MVC-architecture"""
from decimal import Decimal
from django.db import models

class Cryptocoin(models.Model):
    """Attributes are not final yet, depends on API use"""
    symbol = models.CharField(max_length=4)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'))
    amount = models.DecimalField(max_digits=12, decimal_places=3, default=Decimal('0.000'))
    def __str__(self):
        return self.symbol
        
"""Models, as Model in MVC-architecture"""
from django.db import models

class Cryptocoin(models.Model):
    """Attributes are not final yet, depends on API use"""
    alias = models.CharField(max_length=4)
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    ranking = models.PositiveIntegerField
    market_cap = models.PositiveIntegerField
    def __str__(self):
        return self.name

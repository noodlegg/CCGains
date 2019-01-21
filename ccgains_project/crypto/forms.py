from django import forms
from .models import Cryptocoin

class CoinForm(forms.ModelForm):
    class Meta:
        model = Cryptocoin
        fields = ('amount', 'price',)
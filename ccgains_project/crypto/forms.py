"""Forms to allow user input to save to model"""
from django import forms
from .models import Cryptocoin

class CoinForm(forms.ModelForm):
    """Form for the Cryptocoin model"""
    class Meta:
        model = Cryptocoin
        fields = ('amount', 'price',)

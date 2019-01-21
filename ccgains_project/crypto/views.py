"""Views, as Controller in MVC-architecture"""
import requests
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .models import Cryptocoin

def index(request):
    """Gets JSON data from API as context for index.html"""
    url_coins = 'https://chasing-coins.com/api/v1/top-coins/50'
    top_coin_list = requests.get(url_coins).json()
    url_market = 'https://chasing-coins.com/api/v1/std/marketcap'
    market_cap = requests.get(url_market).json()
    context = {
        'top_coin_list': top_coin_list,
        'market_cap': market_cap,
        }
    return render(request, 'crypto/index.html', context)

def detail(request, coin_symbol):
    """
    Gets JSON data from API depending on coin symbol
    that is retrieved from /crypto/urls.py
    """
    url_stats = 'https://chasing-coins.com/api/v1/std/coin/' + coin_symbol
    url_logo = 'https://chasing-coins.com/api/v1/std/logo/' + coin_symbol
    coin_stats = requests.get(url_stats).json()
    user_coins = Cryptocoin.objects.filter(symbol=coin_symbol)
    context = {
        'coin_stats': coin_stats,
        'coin_logo': url_logo,
        'coin_symbol': coin_symbol,
        'user_coins': user_coins,
        }
    return render(request, 'crypto/detail.html', context)

class SignUp(generic.CreateView):
    """!comment missing"""
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
        
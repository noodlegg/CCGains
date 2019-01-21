"""Views, as Controller in MVC-architecture"""
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.views import generic
from .models import Cryptocoin
from .forms import CoinForm

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
    # Filter all coins by the corresponding symbol, i.e. 'ETH' or 'BTC'
    user_coins = Cryptocoin.objects.filter(symbol=coin_symbol)
    # To save input form if it was submitted
    if request.method == "POST":
        form = CoinForm(request.POST)
        if form.is_valid():
            coinform = form.save(commit=False)
            coinform.symbol = coin_symbol
            coinform.save()
            return HttpResponseRedirect(reverse("crypto:detail", args=(coin_symbol,)))
    else:
        form = CoinForm()
    # context sent to the detail.html template
    context = {
        'coin_stats': coin_stats,
        'coin_logo': url_logo,
        'coin_symbol': coin_symbol,
        'user_coins': user_coins,
        'form': form,
        }
    return render(request, 'crypto/detail.html', context)

def detail_edit(request, coin_symbol):
    """Edit user coins"""
    user_coins = Cryptocoin.objects.filter(symbol=coin_symbol).first()
    if request.method == "POST":
        form = CoinForm(request.POST, instance=user_coins)
        if form.is_valid():
            coinform = form.save(commit=False)
            coinform.symbol = coin_symbol
            coinform.save()
            return redirect('crypto:detail', coin_symbol=coin_symbol)
    else:
        form = CoinForm(instance=user_coins)
    return render(request, 'crypto/detail.html', {'form': form})

class SignUp(generic.CreateView):
    """!comment missing"""
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
        
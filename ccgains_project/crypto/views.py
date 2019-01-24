"""Views, as Controller in MVC-architecture"""
import decimal
import requests
from django.shortcuts import render, get_object_or_404
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
    url_market = 'https://chasing-coins.com/api/v1/std/marketcap'
    market_cap = requests.get(url_market).json()
    url_stats = 'https://chasing-coins.com/api/v1/std/coin/' + coin_symbol
    url_logo = 'https://chasing-coins.com/api/v1/std/logo/' + coin_symbol
    url_highlow = 'https://chasing-coins.com/api/v1/std/highlow/' + coin_symbol
    coin_stats = requests.get(url_stats).json()
    coin_highlow = requests.get(url_highlow).json()
    # Filter all coins by the corresponding symbol, i.e. 'ETH' or 'BTC'
    if(request.user.is_authenticated):
        user_coins = Cryptocoin.objects.filter(symbol=coin_symbol).filter(userid=request.user.id)
    # Calculate the sum of the user's coins
    sum_value = 0
    sum_value_current = 0
    sum_ath = 0
    sum_month_h = 0
    sum_month_l = 0
    for coins in user_coins:
        sum_value += (coins.amount * coins.price)
        sum_value_current += (coins.amount * decimal.Decimal(coin_stats['price']))
        sum_ath += (coins.amount * decimal.Decimal(coin_highlow['ath']['price_usd']))
        sum_month_h += (coins.amount * decimal.Decimal(coin_highlow['month_high']['price_usd']))
        sum_month_l += (coins.amount * decimal.Decimal(coin_highlow['month_low']['price_usd']))
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
        'market_cap': market_cap,
        'coin_stats': coin_stats,
        'coin_logo': url_logo,
        'coin_symbol': coin_symbol,
        'user_coins': user_coins,
        'form': form,
        'sum_value': sum_value,
        'sum_value_current': sum_value_current,
        'sum_ath': sum_ath,
        'sum_month_h': sum_month_h,
        'sum_month_l': sum_month_l,
        }
    return render(request, 'crypto/detail.html', context)

def detail_edit(request, coin_symbol, coin_id):
    """Edit user coins"""
    user_coins = get_object_or_404(Cryptocoin, symbol=coin_symbol, id=coin_id)
    url_logo = 'https://chasing-coins.com/api/v1/std/logo/' + coin_symbol
    url_market = 'https://chasing-coins.com/api/v1/std/marketcap'
    market_cap = requests.get(url_market).json()
    if request.method == "POST":
        form = CoinForm(request.POST, instance=user_coins)
        if form.is_valid():
            coinform = form.save(commit=False)
            coinform.symbol = coin_symbol
            coinform.save()
            return HttpResponseRedirect(reverse("crypto:detail", args=(coin_symbol,)))
    else:
        form = CoinForm(instance=user_coins)
    context = {
        'form': form,
        'coin_logo': url_logo,
        'coin_symbol': coin_symbol,
        'market_cap': market_cap,
    }
    return render(request, 'crypto/detail_edit.html', context)

def detail_delete(request, coin_symbol, coin_id):
    """Delete user coins"""
    user_coins = get_object_or_404(Cryptocoin, symbol=coin_symbol, id=coin_id)
    url_logo = 'https://chasing-coins.com/api/v1/std/logo/' + coin_symbol
    url_market = 'https://chasing-coins.com/api/v1/std/marketcap'
    market_cap = requests.get(url_market).json()
    if request.method == "POST":
        user_coins.delete()
        return HttpResponseRedirect(reverse("crypto:detail", args=(coin_symbol,)))
    context = {
        'coin_logo': url_logo,
        'coin_symbol': coin_symbol,
        'user_coins': user_coins,
        'market_cap': market_cap,
    }
    return render(request, 'crypto/detail_delete.html', context)

class SignUp(generic.CreateView):
    """!comment missing"""
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
        
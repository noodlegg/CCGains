import requests

def show_market_cap(request):
    url_market = 'https://chasing-coins.com/api/v1/std/marketcap'
    market_cap = requests.get(url_market).json()
    return {
        'market_cap': market_cap,
    }
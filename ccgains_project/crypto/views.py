"""Views, as Controller in MVC-architecture"""
from django.views import generic
from django.shortcuts import render
import requests
from .models import Cryptocoin

def index(request):
    """Gets JSON data from API as context for index.html"""
    url = 'https://chasing-coins.com/api/v1/top-coins/50'
    top_coin_list = requests.get(url).json()
    context = {'top_coin_list': top_coin_list}
    return render(request, 'crypto/index.html', context)

class DetailView(generic.DetailView):
    """Shows details of selected cryptocoin"""
    model = Cryptocoin
    template_name = 'crypto/detail.html'

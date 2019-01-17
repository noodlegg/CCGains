"""Views, as Controller in MVC-architecture"""
from django.views import generic
from .models import Cryptocoin

class IndexView(generic.ListView):
    """Index lists top cryptocoins"""
    template_name = 'crypto/index.html'
    context_object_name = 'top_coin_list'

    def get_queryset(self):
        return Cryptocoin.objects.all()

class DetailView(generic.DetailView):
    """Shows details of selected cryptocoin"""
    model = Cryptocoin
    template_name = 'crypto/detail.html'

"""Handles URLs"""
from django.urls import path
from . import views

app_name = 'crypto'
urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:symbol>/', views.DetailView.as_view(), name='detail'),
]

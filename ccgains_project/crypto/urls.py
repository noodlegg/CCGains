"""Handles URLs"""
from django.urls import path
from . import views


app_name = 'crypto'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('<coin_symbol>/', views.detail, name='detail'),
]

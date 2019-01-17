"""Allows modification of models if logged in"""
from django.contrib import admin
from .models import Cryptocoin

admin.site.register(Cryptocoin)

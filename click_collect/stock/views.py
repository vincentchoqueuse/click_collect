from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Market

class MarketListView(ListView):
    model = Market

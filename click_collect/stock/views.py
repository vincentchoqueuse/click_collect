from django.shortcuts import render
from .models import Market
from django.views.generic.list import ListView

class MarketListView(ListView):
	model=Market


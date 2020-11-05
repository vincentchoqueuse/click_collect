from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Bucket
from stock.models import Market
from django.urls import reverse
from django.shortcuts import get_object_or_404

class BucketCreateView(CreateView):
    model = Bucket
    fields = ["client_name","market","quantity","email"]

    def create_form(self, *args, **kwargs):
        form = super().create_form(*args, **kwargs)
        form.instance.market= get_object_or_404(Market,pk=self.kwargs['pk'])
        print(form.instance.market)
        return form


    def get_success_url(self):
        return reverse('market_list')
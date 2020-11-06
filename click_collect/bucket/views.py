from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView
from .models import Bucket, BucketItem
from stock.models import Item, Product, Market
from .forms import BucketItemForm
from django.forms import formset_factory
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect


class MarketListView(ListView):
    model = Market


class BucketItemFormView(FormView):
    template_name = "bucket/bucket_list.html"
    form_class = formset_factory(BucketItemForm,extra = 0)
    success_url = "checkout/"

    def get_market(self):
        return get_object_or_404(Market,pk=self.kwargs.get('market_pk'))

    def get_initial(self):
        initial = []
        object_list = Item.objects.filter(market=self.get_market())
        for object in object_list:
            initial.append({'product': object.product.id,'quantity':0})
        return initial

    def form_valid(self, formset):
        data = []
        for form in formset:
            if form.cleaned_data["quantity"] > 0:
                data.append({"product":form.cleaned_data["product"],"quantity":form.cleaned_data["quantity"]})
        self.request.session["cart"] = data    # the data is stored in session
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        market = self.get_market()
        object_list = Item.objects.filter(market=market)
        context["market"] = market
        context["item_object_and_formset"] = zip(object_list,context["form"])
        return context


class BucketCreateView(CreateView):
    model = Bucket
    fields = ["client_name","email"]
    success_url = '/thanks/'

    def get_object_list(self):
        item_list = self.request.session.get('cart', [])
        object_list = []
        for item in item_list:
            product =  get_object_or_404(Product,pk=item["product"])
            object_list.append(BucketItem(product=product,quantity=item["quantity"]))
        return object_list

    def form_valid(self, form):
        # save the bucket in dB
        bucket_object = form.save(commit=False)
        bucket_object.market = get_object_or_404(Market,pk=self.kwargs.get('market_pk'))
        bucket_object.save()
        # save all the BucketItem in dB
        object_list = self.get_object_list()
        for bucket_item in object_list :
            bucket_item.bucket=bucket_object
            bucket_item.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = self.get_object_list()
        return context

class BucketCreatedView(TemplateView):
    template_name = "bucket/bucket_created.html"
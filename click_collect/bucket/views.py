from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from .models import Bucket, BucketItem
from stock.models import Item, Product, Market
from .forms import BucketItemForm, ClientForm
from django.forms import formset_factory
from django.http import HttpResponseRedirect



class MarketListView(ListView):
    model = Market


class BucketItemFormView(FormView):
    template_name = "bucket/bucket_list.html"
    form_class = formset_factory(BucketItemForm,extra = 0)
    success_url = "/checkout/"

    def get_initial(self):
        initial = []
        market_pk = self.kwargs.get('market_pk')
        object_list = Item.objects.filter(market_id=market_pk)
        for object in object_list:
            product_id = object.product.id
            try:
                quantity = self.request.session["cart"][str(market_pk)]["products"][str(product_id)]["quantity"]
            except:
                quantity = 0
            initial.append({'product': product_id,'quantity':quantity})
        return initial

    def form_valid(self, formset):
        data = {}
        total_price_cart = 0
        for form in formset:
            quantity = form.cleaned_data["quantity"]
            if quantity > 0:
                product = get_object_or_404(Product,pk=form.cleaned_data["product"])
                total_price = quantity*product.price
                data[product.id] = {"name":product.name,"quantity":quantity,"price":product.price,"total_price":total_price}
                total_price_cart += total_price

        # store data in session
        market = get_object_or_404(Market,pk=self.kwargs.get('market_pk'))
        cart = {market.id: {"products":data,"total_price":total_price_cart,"market_name":market.name}}

        if self.request.session.get("cart") is None:
            self.request.session["cart"]={}  
        self.request.session.update({"cart":cart})

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_list = Item.objects.filter(market_id=self.kwargs.get('market_pk'))
        context["item_object_and_formset"] = zip(object_list,context["form"])
        return context


class BucketCreateView(FormView):
    template_name = "bucket/bucket_form.html"
    form_class = ClientForm
    success_url = '/thanks/'

    def form_valid(self, form):
        object_list = self.request.session.get('cart', [])


        for market_id,market_item in object_list.items() :
            bucket = Bucket(market_id = market_id,client_name=form.cleaned_data["name"],email=form.cleaned_data["email"])
            bucket.save()
            for product_id,product_item in market_item["products"].items():
                bucket_item = BucketItem(bucket=bucket,product_id=product_id,quantity=product_item["quantity"],price=product_item["price"])
                bucket_item.save()
        #remove cart
        self.request.session.pop("cart")
        return HttpResponseRedirect(self.get_success_url())

class BucketCreatedView(TemplateView):
    template_name = "bucket/bucket_created.html"
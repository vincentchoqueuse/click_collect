from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from .models import Bucket, BucketItem
from stock.models import Item, Product, Market
from .forms import BucketItemForm
from django.forms import formset_factory
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect


class MarketListView(ListView):
    model = Market


def manage_buckets(request,market_pk):
    BucketItemFormSet = formset_factory(BucketItemForm,extra = 0)
    object_list = Item.objects.filter(market__id=market_pk)
    market = get_object_or_404(Market,pk=market_pk)
    if request.method == 'POST':
        formset = BucketItemFormSet(request.POST, request.FILES)
        if formset.is_valid():
            # go here if the formset is valid
            data = [] # we create a data to store the product and the quantity
            for form in formset:
                if form.cleaned_data["quantity"] > 0:
                    data.append({"product":form.cleaned_data["product"],"quantity":form.cleaned_data["quantity"]})
            request.session["cart"] = data    # the data is stored in session
            # go to checkout (cucker createview)
            return HttpResponseRedirect('checkout/')
    else:
        initial = []
        for object in object_list:
            initial.append({'product': object.product.id,'quantity':0})
        formset = BucketItemFormSet(initial = initial)
    return render(request, 'bucket/bucket_list.html', {'item_object_and_formset': zip(object_list,formset),"formset":formset,"market":market})


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = self.get_object_list()
        return context

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


class BucketCreatedView(TemplateView):
    template_name = "bucket/bucket_created.html"
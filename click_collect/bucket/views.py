from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from .forms import BucketItemForm, ClientForm
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from stock.models import Market
from .cart import Cart


class MarketListView(ListView):
    model = Market

class BucketItemFormView(FormView):
    template_name = "bucket/bucket_list.html"
    form_class = formset_factory(BucketItemForm,extra=0)
    success_url = "/checkout/"

    def get_initial(self):
        market_pk = self.kwargs.get('market_pk')
        cart = Cart(self.request.session)
        initial = cart.get_market(market_pk)
        return initial

    def form_valid(self, formset):
        market_pk = self.kwargs.get('market_pk')
        cart = Cart(self.request.session)
        cart.set_market(market_pk,formset)
        return HttpResponseRedirect(self.get_success_url())

class BucketCreateView(FormView):
    template_name = "bucket/bucket_form.html"
    form_class = ClientForm
    success_url = '/thanks/'

    def form_valid(self, form):
        cart = Cart(self.request.session)
        cart.save(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request.session)
        context['total_price'] = cart.total_price()
        return context

class BucketCreatedView(TemplateView):
    template_name = "bucket/bucket_created.html"
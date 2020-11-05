from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from .models import Bucket
from stock.models import Market
from django.urls import reverse
from django.shortcuts import get_object_or_404

class BucketCreateView(CreateView):
    model = Bucket
    fields = ["client_name","quantity","email"]

    def form_valid(self, form):
        # we add the market manually when the form is valid
        form.instance.market = get_object_or_404(Market,pk=self.kwargs['market'])
        return super(BucketCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        # we pass the market to the template
        context = super(BucketCreateView, self).get_context_data(**kwargs)
        context['market'] = get_object_or_404(Market,pk=self.kwargs['market'])
        return context

    def get_success_url(self):
        return reverse('bucket_created')



class BucketCreatedView(TemplateView):
    template_name = "bucket/bucket_created.html"
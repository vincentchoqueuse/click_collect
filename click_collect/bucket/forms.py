from django import forms
from .models import BucketItem
from stock.models import Product, Item
from django.forms.formsets import formset_factory
from django.shortcuts import  get_object_or_404
from django.forms import ModelForm


class BucketItemForm(forms.Form):

    product_pk = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.FloatField(initial=0)

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get('initial', None):
            product_object = Product.objects.get(pk = kwargs["initial"]["product_pk"])
            if  product_object.unit  == 1:
                self.fields['quantity'].widget = forms.NumberInput(attrs={'class': "form-control form-control-sm quantity",'step': '1'})   
                self.fields['quantity'].help_text = '/ unit'   
            if  product_object.unit  == 2:
                self.fields['quantity'].widget = forms.NumberInput(attrs={'class': "form-control form-control-sm quantity",'step': '0.5'})  
                self.fields['quantity'].help_text = '/ kg' 
            if  product_object.unit  == 3:
                self.fields['quantity'].widget = forms.NumberInput(attrs={'class': "form-control form-control-sm quantity",'step': '0.25'})      
                self.fields['quantity'].help_text = '/ kg' 
            self.instance = product_object


class ClientForm(forms.Form):

    name = forms.CharField()
    email = forms.EmailField()

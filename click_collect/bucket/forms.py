from django import forms
from stock.models import Product
from django.forms.formsets import formset_factory
from django.shortcuts import  get_object_or_404

class BucketItemForm(forms.Form):

    product = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.FloatField(initial=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get('initial', None):
            product = get_object_or_404(Product,pk=kwargs['initial']['product'] )
            if product.unit  == 1:
                self.fields['quantity'].widget = forms.NumberInput(attrs={'class': "form-control form-control-sm",'step': '1'})   
                self.fields['quantity'].help_text = '/ unit'   
            if product.unit  == 2:
                self.fields['quantity'].widget = forms.NumberInput(attrs={'class': "form-control form-control-sm",'step': '0.5'})  
                self.fields['quantity'].help_text = '/ kg' 
            if product.unit  == 3:
                self.fields['quantity'].widget = forms.NumberInput(attrs={'class': "form-control form-control-sm",'step': '0.25'})      
                self.fields['quantity'].help_text = '/ kg' 
        
        #self.fields['my_checkbox'].widget.attrs['onclick'] = 'return false;'


class ClientForm(forms.Form):

    name = forms.CharField()
    email = forms.EmailField()

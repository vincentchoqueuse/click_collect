from django import forms
from django.forms.formsets import formset_factory

class BucketItemForm(forms.Form):

    product = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.FloatField(initial=0,widget=forms.NumberInput(attrs={'class': "form-control form-control-sm"}))

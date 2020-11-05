from django.contrib import admin

# Register your models here.
from .models import Product, Stock

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['name','image' ]


class StockAdmin(admin.ModelAdmin):
    model = Stock
    list_display = ['name','quantity','date']

admin.site.register(Product,ProductAdmin)
admin.site.register(Stock,StockAdmin)

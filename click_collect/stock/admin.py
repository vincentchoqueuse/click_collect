from django.contrib import admin

# Register your models here.
from .models import Product, Item, Market

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['name','image','quantity','price','unit']

class ItemInline(admin.TabularInline):
    model = Item
    extra = 3
    fields = ('product', 'quantity', 'description')


class MarketAdmin(admin.ModelAdmin):
    model = Market
    list_display = ['name','date_market','deadline_cart','city']
    inlines = (
        ItemInline,
        )

admin.site.register(Product,ProductAdmin)
admin.site.register(Market,MarketAdmin)
from django.contrib import admin
from .models import Product,Stock,Market

class ProductAdmin(admin.ModelAdmin):
	model =Product
	list_display=['name','image']

class StockAdmin(admin.ModelAdmin):
	model =Stock
	list_display=['name','quantity','date',]

class MarketAdmin(admin.ModelAdmin):
	model=Market
	list_display=['name','date','city',]

admin.site.register(Product,ProductAdmin)
admin.site.register(Stock,StockAdmin)
admin.site.register(Market,MarketAdmin)
# Register your models here.

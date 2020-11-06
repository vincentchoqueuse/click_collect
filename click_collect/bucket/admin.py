from django.contrib import admin

# Register your models here.
from .models import Bucket, BucketItem

class ItemInline(admin.TabularInline):
    model = BucketItem
    fields = ('product', 'quantity')
    readonly_fields = ('total_price',)
    extra = 0

class BucketAdmin(admin.ModelAdmin):
    model = Bucket
    list_display = ['client_name','email','market','date','total_price','confirmed']
    list_filter = ['market']
    inlines = (
        ItemInline,
        )




admin.site.register(Bucket,BucketAdmin)
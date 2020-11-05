from django.contrib import admin

# Register your models here.
from .models import Bucket

class BucketAdmin(admin.ModelAdmin):
    model = Bucket
    list_display = ['client_name','email','market' ]


admin.site.register(Bucket,BucketAdmin)
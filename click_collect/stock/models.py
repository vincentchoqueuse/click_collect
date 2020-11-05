from django.db import models
from django.utils.html import mark_safe

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images/", null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.name)

    def image_tag(self):
        from django.utils.html import escape
        return mark_safe('<img src="{}" width="150" height="150" />'.format(self.image))

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

class Stock(models.Model):
    name = models.CharField(max_length=200)
    product = models.ForeignKey("Product",on_delete=models.CASCADE)
    date = models.DateField()
    quantity = models.IntegerField(default=0)

class Market(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    date = models.DateTimeField()
    stock = models.ManyToManyField(Stock)
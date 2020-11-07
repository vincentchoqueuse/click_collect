from django.db import models
from django.utils.html import mark_safe

TYPE_CHOICES = (
    (1, "Pièce"),
    (2, "kilo"),
    (3, "kilo")
)

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    unit = models.IntegerField(choices=TYPE_CHOICES, default=1) 

    def __str__(self):
        return '{}'.format(self.name)

    @property
    def image_url(self):
        if self.image:
            value = self.image.url
        else:
            value ="#"
        return value

class Market(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    deadline_cart = models.DateTimeField()
    date_market = models.DateTimeField()
    
    def __str__(self):
        return '{}'.format(self.name)

class Item(models.Model):
    market = models.ForeignKey("Market",on_delete=models.CASCADE)
    description = models.CharField(max_length=30,null=True, blank=True)
    product = models.ForeignKey("Product",on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return '{}'.format(self.product)

    def remaining_quantity(self):
        return 3
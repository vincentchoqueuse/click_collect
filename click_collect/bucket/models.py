from django.db import models
from stock.models import Market

# Create your models here.
class Bucket(models.Model):
    client_name = models.CharField(max_length=200)
    market = models.ForeignKey(Market ,on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    email = models.EmailField()
    confirmed = models.BooleanField(default=False)

    def total_price(self):
        price = 0
        for bucket_item in self.bucketitem_set.all():
            price += bucket_item.total_price()
        return round(price,2)


class BucketItem(models.Model):
    bucket = models.ForeignKey("Bucket",on_delete=models.CASCADE)
    product = models.ForeignKey("stock.Product",on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0)

    def __str__(self):
        return '{}'.format(self.product)

    def total_price(self):
        return self.price*self.quantity
from django.db import models
from stock.models import Market

# Create your models here.
class Bucket(models.Model):
    client_name = models.CharField(max_length=200)
    market = models.ForeignKey(Market ,on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    quantity = models.IntegerField(default=0)
    email = models.EmailField()
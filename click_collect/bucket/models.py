from django.db import models


class Bucket(models.Model):
	client_name = models.CharField(max_length=200)
	market = models.ForeignKey("stock.Market", on_delete=models.CASCADE)
	date = models.DateField(auto_now=True)
	quantity = models.IntegerField(default=0)
	email= models.EmailField()

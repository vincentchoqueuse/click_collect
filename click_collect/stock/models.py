from django.db import models

# Create your models here.
class Product(models.Model):
	name = models.CharField(max_length=200)
	image = models.ImageField(upload_to="images/", null=True, blank=True)

	def __str__(self):
		return self.name

class Stock(models.Model):
	name = models.CharField(max_length=200)
	product = models.ForeignKey('Product',on_delete=models.CASCADE)
	date = models.DateTimeField()
	quantity = models.IntegerField(default=0)

class Market(models.Model):
	name = models.CharField(max_length=200)
	city = models.CharField(max_length=200)
	date = models.DateField()
	stock = models.ManyToManyField(Stock)


from django.db import models
from django.utils import timezone

# Create your models here.

class Categories(models.Model):
	category = models.CharField(max_length=200)
	created_at = models.DateTimeField(default=timezone.now)

class News(models.Model):
    title = models.CharField(max_length=200)
    contents = models.CharField(max_length=500, null=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, default=1)
    pub_date = models.DateTimeField(default=timezone.now)

class SalesSentences(models.Model):
	train_subway_station = models.CharField(max_length=10)
	price = models.DecimalField(max_digits=5, decimal_places=1)
	floor_plan = models.CharField(max_length=10)
	property_category = models.CharField(max_length=10)
	sentence_content = models.CharField(max_length=40)

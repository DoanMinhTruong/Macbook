from django.db import models

# Create your models here.
class Mac(models.Model):
    name = models.CharField(max_length = 255)
    img = models.ImageField(upload_to = 'uploads/')
    price = models.FloatField(verbose_name="mac price")
    rating = models.IntegerField(default=0)
    informations = models.CharField(max_length = 255)
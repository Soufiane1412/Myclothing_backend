from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_place=2)
    image_url = models.URLField(max_length=200)

    def __str__(self):
        return self.name
    
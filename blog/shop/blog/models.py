from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=30)
    quantity = models.IntegerField(default=0)
    price = models.IntegerField()
    image = models.ImageField()
    description = models.TextField(blank = False)
    pub_date = models.DateTimeField(auto_now_add=True)

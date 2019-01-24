from django.db import models
from django import forms
from django.contrib.auth.models import User

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(null = False, max_length=150)
    price = models.IntegerField(default=0)
    description = models.TextField(null = False, max_length=500)
    picture_url = models.CharField(null = True,max_length=150)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username","email","password"]

class Cart(models.Model):
    cart_id = models.AutoField(primary_key = True)
    userid = models.CharField(null=False, max_length=150)
    product_id = models.IntegerField(default=0)
    amount=models.IntegerField(default=0)
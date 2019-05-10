from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','quantity')
    ordering = ('-pub_date',)

admin.site.register(Product, ProductAdmin)
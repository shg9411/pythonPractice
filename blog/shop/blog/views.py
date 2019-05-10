from django.shortcuts import render, render_to_response
from .models import Product
from django.views.generic import ListView
from django.views.generic import DetailView


class ProductListView(ListView):
    ordering = ['-pub_date']
    model = Product
    paginate_by = 6


class ProductDetailView(DetailView):
    model = Product
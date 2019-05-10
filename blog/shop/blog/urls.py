from django.urls import path
from .views import ProductListView as PL
from .views import ProductDetailView as PD

urlpatterns = [
    path('', PL.as_view(), name='index'),
    path('<int:pk>/', PD.as_view(), name='product-detail'),
]

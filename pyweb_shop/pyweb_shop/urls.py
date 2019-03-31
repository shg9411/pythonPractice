from django.contrib import admin
from django.urls import path
from shop import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('product_list', views.product_list),
    path('product_detail', views.product_detail),
    path('login', views.login_check, name='login'),
    path('join/', views.join, name='join'),
    path('logout/', views.logout, name='logout'),
    path('cart_list', views.cart_list),
    path('cart_insert', views.cart_insert),
    path('cart_update', views.cart_update),
    path('cart_del', views.cart_del),
    path('cart_del_all', views.cart_del_all),
    path('product_write', views.product_write),
    path('product_insert', views.product_insert),
    path('product_edit', views.product_edit),
    path('product_update', views.product_update),
    path('product_delete', views.product_delete),
]

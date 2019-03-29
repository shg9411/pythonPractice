from django.urls import path, include
from . import views

app_name = 'elections'
urlpatterns = [
    path('', views.index, name='home'),
    path('areas/<str:area>/', views.areas),
    path('polls/<int:poll_id>/', views.polls),
    path('areas/<str:area>/results', views.results),
    path('candidates/<str:name>/', views.candidates),
]

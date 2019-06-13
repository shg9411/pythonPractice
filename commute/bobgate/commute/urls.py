from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from django.conf import settings
from django.conf.urls.static import static


app_name = 'commute'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_view.LoginView.as_view(), name='login'),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    path('register/', views.SignUp.as_view(), name='register'),
    path('myWork/<date>/',views.myWork_detail, name = 'myWork_detail'),
    path('myWork/<date>/add/',views.addWork, name = 'addWork'),
    path('myWork/',views.CalendarView.as_view(), name = 'myWork'),
    path('myWork/<date>/edit/',views.editWork, name = 'editWork'),
    path('board/',views.BoardLV.as_view(), name = 'board'),
    path('board/add/',views.addBoard, name = 'addBoard'),
    path('board/<int:pk>/', views.BoardDV.as_view(), name = 'board_detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
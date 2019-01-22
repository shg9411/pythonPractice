from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import url, include
from board import views


urlpatterns = [
    path('admin/', admin.site.urls),
    #게시물 목록
    path('',views.list),
    path('write',views.write),
    path('insert',views.insert),
    path('download',views.download),
    path('detail',views.detail),
    path('detail/',views.detail),
    path('reply_insert',views.reply_insert),
    path('update',views.update),
    path('delete',views.delete),
]

#디버그 툴바 관련 url mapping
if settings.DEBUG: #settings.py의 디버그 변수 설정
    import debug_toolbar #디버그 툴바 기능을 가져옴
    #디버그 툴바의 url패턴 정의
    urlpatterns += [
        url(r'^__debug__/',include(debug_toolbar.urls)),
    ]
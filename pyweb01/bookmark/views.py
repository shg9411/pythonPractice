from django.shortcuts import render,render_to_response
from bookmark.models import Bookmark

def home(request):
    urlList = Bookmark.objects.order_by("title")
    urlCount = Bookmark.objects.all().count()
    return render_to_response("list.html",{"urlList":urlList,"urlCount":urlCount})

def detail(request):
    addr = request.GET["url"]
    dto = Bookmark.objects.get(url=addr)
    return render_to_response("detail.html",{"dto":dto})
from django.shortcuts import render_to_response,redirect
from django.views.decorators.csrf import csrf_exempt

from guestbook.models import Guestbook

from django.db.models import Q

# Create your views here.
@csrf_exempt
def list(request):
    try:
        msg=request.GET["msg"]
    except:
        msg=""
    try:
        searchkey = request.POST["searchkey"]
    except:
        searchkey = "name"
    try:
        search=request.POST["search"]
    except:
        search=""

    if searchkey=="name_content":
        gbCount=Guestbook.objects.filter(Q(name__contains=search)|Q(content__contains=search)).count()
    elif searchkey=="name":
        gbCount = Guestbook.objects.filter(name__contains = search).count()
    elif searchkey =="content":
        gbCount = Guestbook.objects.filter(content__contains = search).count()

    if searchkey=="name_content":
        gbList = Guestbook.objects.filter(Q(name__contains=search)|Q(content__contains=search)).order_by("-idx")
    elif searchkey=="name":
        gbList = Guestbook.objects.filter(name__contains = search).order_by("-idx")
    elif searchkey=="content":
        gbList = Guestbook.objects.filter(content__contains = search).order_by("-idx")
    return render_to_response("list.html",{"gbList":gbList,"gbCount":gbCount,"searchkey":searchkey,
                                           "search":search, "msg":msg})

def write(request):
    return render_to_response("write.html")

@csrf_exempt
def insert(request):
    dto = Guestbook(name=request.POST["name"],
                    email=request.POST["email"],
                    passwd=request.POST["passwd"],
                    content=request.POST["content"])
    dto.save()
    return redirect("/")

@csrf_exempt
def passwd_check(request):
    id = request.POST["idx"]
    pwd = request.POST["passwd"]
    dto = Guestbook.objects.get(idx=id)
    if dto.passwd==pwd:
        return render_to_response("edit.html",{"dto":dto})
    else:
        return redirect("/?msg=error")

@csrf_exempt
def update(request):
    id = request.POST["idx"]
    dto = Guestbook(idx = id, name=request.POST["name"],
                    email=request.POST["email"],
                    passwd=request.POST["passwd"],
                    content=request.POST["content"])
    dto.save()
    return redirect("/")

@csrf_exempt
def delete(request):
    id = request.POST["idx"]
    Guestbook.objects.get(idx=id).delete()
    return redirect("/")
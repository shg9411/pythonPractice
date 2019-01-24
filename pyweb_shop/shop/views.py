import math
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.http import urlquote
from django.shortcuts import render, render_to_response,redirect
from .forms import LoginForm, UserForm
from django.contrib.auth.models import User
from django.contrib.auth import(
authenticate,
login as django_login,
logout as django_logout,
)
from .models import Product, Cart

UPLOAD_DIR="C:/Users/USER/Desktop/pythonPractice/pyweb_shop/shop/static/images/"

def home(request):
    if not request.user.is_authenticated:
        data = {"username":request.user,
                "is_authenticated":request.user.is_authenticated}
    else:
        data = {"last_login":request.user.last_login,
                "username":request.user.username,
                "password":request.user.password,
                "is_authenticated":request.user.is_authenticated}
    return render(request, "index.html",context={"data":data})

def product_list(request):
    count = Product.objects.count()
    productList = Product.objects.order_by("product_name")
    return render_to_response("product_list.html",{"productList":productList,"count":count})

def product_detail(request):
    pid = request.GET["product_id"]
    dto = Product.objects.get(product_id=pid)
    return render_to_response("product_detail.html",{"dto":dto,"range":range(1,21)})

@csrf_exempt
def cart_insert(request):
    uid =request.session.get("userid","")
    if uid!="":
        dto = Cart(userid=uid,
                   product_id=request.POST["product_id"],
                   amount=request.POST["amount"])
        dto.save()
        return redirect("/cart_list")
    else:
        return redirect("/login")

def login_check(request):
    if request.method=="POST":
        form = LoginForm(request.POST)
        name = request.POST["username"]
        pwd = request.POST["password"]
        user = authenticate(username=name, password=pwd)
        if user is not None:
            django_login(request, user)
            request.session["userid"] = name
            return redirect("/")
        else:
            return render_to_response("index.html",{"msg":"로그인 실패... 다시 시도해 보세요."})
    else:
        form = LoginForm()
        return render(request, "login.html",{"form":form})

def join(request):
    if request.method=="POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user=User.objects.create_user(**form.cleaned_data)
            django_login(request, new_user)
            return redirect("/")
        else:
            return render_to_response("index.html",
                                      {"msg":"회원가입 실패... 다시 시도해 보세요."})
    else:
        form = UserForm()
        return render(request, "join.html",{"form":form})
    return render(request, "index.html")

def logout(request):
    django_logout(request)
    for sesskey in request.session.keys():
        del request.session[sesskey]
    return redirect("/")

def cart_list(request):
    uid = request.session.get("userid","")
    if uid != "":
        cartCount = Cart.objects.count()
        cartList = Cart.objects.raw("""
        select cart_id, userid, amount, c.product_id, product_name, price, amount*price money
        from shop_cart c, shop_product p
        where c.product_id=p.product_id and userid='{0}'
        """.format(uid))
        sumMoney=0
        fee=0
        sum=0
        if cartCount > 0:
            sumRow = Cart.objects.raw("""
            select sum(amount*price) cart_id
            from shop_cart c, shop_product p
            where c.product_id=p.product_id and userid='{0}'
            """.format(uid))
            sumMoney=sumRow[0].cart_id
            if sumMoney != None and sumMoney > 50000:
                fee = 0
            else:
                fee = 2500
            if sumMoney != None:
                sum = sumMoney+fee
            else:
                sumMoney=0
                sum=0
        return render_to_response(
            "cart_list.html",{"cartList":cartList,
                              "cartCount":cartCount,
                              "sumMoney":sumMoney,
                              "fee":fee,
                              "sum":sum})
    else:
        return redirect("/login")

@csrf_exempt
def cart_update(request):
    uid = request.session.get("userid","")
    if uid != "":
        amt = request.POST.getlist("amount")
        cid=request.POST.getlist("cart_id")
        pid=request.POST.getlist("product_id")
        for idx in range(len(cid)):
            dto = Cart(cart_id=cid[idx],
                       userid=uid,
                       product_id=pid[idx],
                       amount = amt[idx])
        dto.save()
        return redirect("/cart_list")
    else:
        return redirect("/login")

@csrf_exempt
def cart_del(request):
    Cart.objects.get(cart_id=request.GET["cart_id"]).delete()
    return redirect("/cart_list")

@csrf_exempt
def cart_del_all(request):
    uid = request.session.get("userid","")
    if uid != "":
        Cart.objects.filter(userid=uid).delete()
        return redirect("/cart_list")
    else:
        return redirect("/login")

def product_write(request):
    uid = request.session.get("userid","")
    if uid=="user":
        return render_to_response("product_write.html")
    else:
        return redirect("/login")

@csrf_exempt
def product_insert(request):
    if "file1" in request.FILES:
        file = request.FILES["file1"]
        file_name = file._name
        fp = open("%s%s" % (UPLOAD_DIR, file_name), "wb")
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()
    else:
        file_name = "-"

    dto = Product(product_name = request.POST["product_name"],
                  description=request.POST["description"],
                  price=request.POST["price"],
                  picture_url = file_name)
    dto.save()
    return redirect("/product_list")

def product_edit(request):
    uid = request.session.get("userid","")
    if uid=="user":
        pid = request.GET["product_id"]
        dto = Product.objects.get(product_id=pid)
        return render_to_response("product_edit.html",{"dto":dto})
    else:
        return redirect("/login")

@csrf_exempt
def product_update(request):
    id = request.POST['product_id']
    dto_src = Product.objects.get(product_id=id)
    p_url = dto_src.picture_url
    if "file1" in request.FILES:
        file = request.FILES["file1"]
        p_url = file._name

        fp = open("%s%s" % (UPLOAD_DIR, p_url), "wb")
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()
    dto_new = Product(product_id = id,
                      product_name=request.POST["product_name"],
                      description=request.POST["description"],
                      price=request.POST["price"],
                      picture_url = p_url)
    dto_new.save()
    return redirect("/product_list")

@csrf_exempt
def product_delete(request):
    Product.objects.get(product_id = request.POST["product_id"]).delete()
    return redirect("/product_list")
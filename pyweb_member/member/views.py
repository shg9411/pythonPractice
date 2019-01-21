from django.shortcuts import render, redirect, render_to_response
from django.views.decorators.csrf import csrf_exempt
from .forms import UserForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    login as django_login,
    logout as django_logout,
)

def home(request):
    if not request.user.is_authenticated: #로그인 하기 전
        data = {"username":request.user,"is_authenticated":request.user.is_authenticated}
    else: #로그인 한 후
        data = {"last_login":request.user.last_login,"username":request.user.username,
                "password":request.user.password,"is_authenticated":request.user.is_authenticated}
    return render(request,"index.html",context={"data":data})

@csrf_exempt
def join(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            #로그인 처리
            django_login(request,new_user)
            return redirect("/")
        else: #중복아이디, 비밀번호 규칙
            return render_to_response("index.html",{"msg":"회원가입 실패... 다시 시도해 보세요."})
    else : #get 방식
        form = UserForm()
        return render(request,"join.html",{"form":form})
    return render(request,"index.html")

def logout(request):
    #django에 내장된 로그아웃 함수
    django_logout(request)
    #시작페이지로 돌아감
    return redirect("/")

def login_check(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        name = request.POST["username"]
        pwd = request.POST["password"]
        #인증
        user = authenticate(username=name, password=pwd)
        if user is not None: #로그인 성공
            django_login(request, user)
            return redirect("/")
        else: #로그인 실패
            return render_to_response("index.html", {"msg":"로그인 실패... 다시 시도해 보세요."})
    else :
        form = LoginForm()
        return render(request,"login.html",{"form":form})

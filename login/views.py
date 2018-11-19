
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from login.forms import LoginForm
from .models import UserLogin
import hashlib


def hash_code(s, salt='mysite'):  # 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

def login_view(request):
    # if user is already logged in go to home page
    # if method is GET render login page else authenticate user
    if request.method == "GET":
       loginform = LoginForm()
       return render(request, 'login.html', {'loginform': loginform})

    if request.method == 'POST':
        form = LoginForm(request.POST)
        # check if the fields are valid
        if form.is_valid():
            name = form.cleaned_data['username']
            pwd = form.cleaned_data['password']
            # authenticates user return None if doesn't exist
            if not UserLogin.objects.filter(username = name):
                return render(request,'login.html',{'msg':"此用户不存在"})
            else:
                pwd = hash_code(pwd)
                if not UserLogin.objects.filter(password=pwd):
                    return render(request,'login.html',{'msg':"密码错误！"})
                else:
                    user = authenticate(username = name,
                                        password = pwd)
                    login(request,user)
                    return render(request,'home.html')

        else:
            return render(request,'login.html',{'msg':"填写格式出错！"})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect("login_url")


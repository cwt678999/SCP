from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import RegisterForm
from .models import CompetitorInfo,OrganizerInfo
from login.models import UserLogin
import hashlib


def hash_code(s, salt='mysite'):  # 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

def register(request):
    if request.method == 'GET':
        registerform = RegisterForm()
        return render(request,"register.html",{'registerform':registerform})

    if request.method == 'POST':
        registerform = RegisterForm()

        if registerform.is_valid():
            name = registerform.cleaned_data['username']
            pwd1 = registerform.cleaned_data['password1']
            pwd2 = registerform.cleaned_data['password2']
            email = registerform.cleaned_data['email']
            user_type = registerform.cleaned_data['type']
            if UserLogin.objects.filter(username = name ):
                return render(request, "register.html", {'registerform': registerform,
                                                         'msg':"此用户名已存在"})
            if CompetitorInfo.objects.filter(email = email) or OrganizerInfo.objects.filter(email = email):
                return render(request, "register.html",{'registerform':registerform,
                                                        'msg':"此邮箱已被注册！"})
            if pwd1 != pwd2:
                return render(request,"register.html",{'registerform':registerform,
                                                       'msg':"两次输入的密码不一致！"})
            else:
                pwd = hash_code(pwd1)
                User.objects.create(username = name, password = pwd)
                UserLogin.objects.create(username = name, password = pwd, type = user_type)

        else:
            return render(request,"register.html",{'registerform':registerform,
                                                   'msg':"填写格式出错"})
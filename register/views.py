from django.shortcuts import render
from .forms import RegisterForm
# Create your views here.
def register(request):
    if request.method == 'GET':
        return render(request,"register.html")

    if request.method == 'POST':
        registerform = RegisterForm()

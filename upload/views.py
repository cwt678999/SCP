from django.shortcuts import render
from .models import Image,File
# Create your views here.
def upload(request):
    if request.method == "GET":
        return render(request,"upload.html")

    if request.method == "POST":
        f = request.FILES.get('img')
        file = File(file = f,
                      username="www")
        file.save()
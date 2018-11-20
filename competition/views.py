from django.shortcuts import render,redirect
from .models import RootCompetition,ChildCompetition
from register.models import OrganizerInfo
from upload.models import Image,File

def createCompetition(request):
    if request.method == "GET"
        return render(requset,"createCompetirion.html")

    if request.methond == 'POST':

        organizer = OrganizerInfo.objects.get(name = request.session['username'])
        rootname = requset.POST.get('rootname')
        description = request.POST.get('description')
        newimage = Image(
            image = request.FILES.get('img'),
            username = request.session['username']
        )
        newimage.save()
        rootcompetition = RootCompetition.objects.create(name = rootname,
                                                         description = description,
                                                         organizer = organizer,
                                                         img = newimage,
                                                         )

        nid = rootcompetition.id
        childcompetitions = request.POST.getlist('childcompetition')
        count = 0
        for item in childcompetitions:
            count = count + 1
        if count >=1 and organizer and rootname and description and newimage:

            return render(requset, "createCompetition.html",{'msg':"success"})
        else:
            return render(request, "createCompetition.html",{'msg':"填写格式出错"})


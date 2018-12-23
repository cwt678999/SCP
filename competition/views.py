from django.shortcuts import render,redirect,HttpResponse
from .models import RootCompetition,ChildCompetition
from register.models import OrganizerInfo,CompetitorInfo
from login.models import UserLogin
from upload.models import Image,File
from django.contrib.auth.decorators import login_required
import datetime


@login_required
def myCompetition(request):
    if request.method == "GET":
        if request.session['type']=="competitor":
            comp_list = []
            userlogin = UserLogin.objects.get(username=request.session['username'])
            my_comp = userlogin.cuser.all()
            for comp in my_comp:
                comp_info = {
                    'id': comp.id,
                    'name': comp.name,
                    'organizer': comp.organizer.all()[0].username,
                    'totalStageNum': comp.totalStageNum,
                    'description': comp.description,
                }
                comp_list.append(comp_info)
            return render(request, "user_center_competition_competitor.html",
                          {'competitionlist': comp_list})

        elif request.session['type']=="organizer":
            comp_list = []
            userlogin = UserLogin.objects.get(username=request.session['username'])
            my_comp = RootCompetition.objects.filter(organizer=userlogin)
            for comp in my_comp:
                comp_info = {
                    'id': comp.id,
                    'name': comp.name,
                    'organizer': userlogin.username,
                    'totalStageNum': comp.totalStageNum,
                    'description': comp.description,
                }
                comp_list.append(comp_info)
            return render(request, "user_center_competition_organizer.html",
                          {'competitionlist':comp_list})


@login_required
def createCompetition(request):
    if request.method == "GET":
        return render(request, "create_competition.html")

    if request.method == "POST":
        userlogin = UserLogin.objects.get(username=request.session['username'])
      #  try:
      #      OrganizerInfo.objects.get(userlogin=userlogin)
      #  except:
      #      return HttpResponse("请完善个人信息")
        rootname = request.POST.get('rootname')
        description = request.POST.get('rootdescription')
        newimage = Image.objects.create(
            image=request.FILES.get('rootimage'),
            username=request.session['username']
        )

        startdatelist = request.POST.getlist('startdate')
        childnamelist = request.POST.getlist('name')
        enddatelist = request.POST.getlist('enddate')
        descriptionlist = request.POST.getlist('description')
        len1 = len(startdatelist)
        len2 = len(childnamelist)
        len3 = len(enddatelist)
        len4 = len(descriptionlist)
        rootcompetition = RootCompetition.objects.create(
                                                         name=rootname,
                                                         description=description,
                                                         totalStageNum=1
                                                         )
        rootcompetition.organizer.add(userlogin)
        rootcompetition.img.add(newimage)
        nid = rootcompetition.id

        if len1 != len2 or len2 != len3 or len3 != len4 or len4 != len1:
            return render(request, "create_competition.html", {'msg': "填写格式出错"})

        for i in range(0,1):
            startdate = datetime.datetime.strptime(startdatelist[i], '%Y-%m-%d')
            enddate = datetime.datetime.strptime(enddatelist[i], '%Y-%m-%d')
            childcompetition = ChildCompetition.objects.create(root_id=nid,
                                                               description=descriptionlist[i],
                                                               name=childnamelist[i],
                                                               startDate=startdate,
                                                               endDate=enddate,
                                                               )
        if userlogin and rootname and description and newimage:

            return render(request, "create_competition.html", {'msg': "success"})
        else:
            return render(request, "create_competition.html", {'msg': "填写格式出错"})


@login_required
def competition_info(request):
    if request.method == 'GET':
        id = request.GET['id']
        comp = RootCompetition.objects.get(id=id)
        child_comp = ChildCompetition.objects.filter(root_id=id)
        child_comp_list = []
        for child in child_comp:
            child_comp_list.append({
                'name': child.name,
                'startDate': child.startDate,
                'endDate': child.endDate,
            })
        organizer = comp.organizer
        name = request.session['username']
        ismember = bool(comp.members.filter(username=name))
        comp_dict = {
            'isMember': ismember,
            'id': id,
            'name': comp.name,
            'organizer': organizer.name,
            'totalStageNum': comp.totalStageNum,
            'description': comp.description,
            'childcompetitionlist': child_comp_list
        }
        return render(request, "competition.html",{'competition': comp_dict})
    if request.method == 'POST':
        name = request.session['username']
        user = UserLogin.objects.get(username=name)
        comp_id = request.POST.get('comp_id')
        comp = RootCompetition.objects.get(id=comp_id)
        comp.members.add(user)
        return redirect('/competition/?id=%s' % comp_id)

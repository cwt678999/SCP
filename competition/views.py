from django.shortcuts import render, redirect, HttpResponse
from .models import RootCompetition, ChildCompetition, Team
from register.models import OrganizerInfo, CompetitorInfo, JudgeInfo
from login.models import UserLogin
from upload.models import Image,File
from django.contrib.auth.decorators import login_required
import datetime


@login_required
def myCompetition(request):
    if request.method == "GET":
        if request.session['type'] == "competitor":
            comp_list = []
            userlogin = UserLogin.objects.get(username=request.session['username'])
            my_comp = userlogin.cuser.all()
            for comp in my_comp:
                comp_info = {
                    'id': comp.id,
                    'name': comp.name,
                    'img': comp.img,
                    'organizer': comp.organizer.username,
                    'totalStageNum': comp.totalStageNum,
                    'description': comp.description,
                }
                comp_list.append(comp_info)
            return render(request, "user_center_competition_competitor.html",
                          {'competitionlist': comp_list})

        elif request.session['type'] == "organizer":
            comp_list = []
            userlogin = UserLogin.objects.get(username=request.session['username'])
            my_comp = RootCompetition.objects.filter(organizer=userlogin)
            for comp in my_comp:
                comp_info = {
                    'id': comp.id,
                    'name': comp.name,
                    'img': comp.img,
                    'organizer': comp.organizer.username,
                    'totalStageNum': comp.totalStageNum,
                    'description': comp.description,
                }
                comp_list.append(comp_info)
            return render(request, "user_center_competition_organizer.html",
                          {'competitionlist':comp_list})
        elif request.session['type'] == "judge":
            comp_list = []
            userlogin = UserLogin.objects.get(username=request.session['username'])
            my_comp = userlogin.juser.all()
            for comp in my_comp:
                comp_info = {
                    'id': comp.id,
                    'name': comp.name,
                    'img': comp.img,
                    'organizer': comp.organizer.username,
                    'totalStageNum': comp.totalStageNum,
                    'description': comp.description,
                }
                comp_list.append(comp_info)
            return render(request, "user_center_competition_judge.html",
                          {'competitionlist': comp_list})

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
        newimage = File.objects.create(
            file=request.FILES.get('rootimage'),
            username=request.session['username']
        )
        newimage.save()
        maxmember = request.POST.get('maxmember')
        startdatelist = request.POST.getlist('startdate')
        childnamelist = request.POST.getlist('name')
        enddatelist = request.POST.getlist('enddate')
        descriptionlist = request.POST.getlist('description')
        len1 = len(startdatelist)
        len2 = len(childnamelist)
        len3 = len(enddatelist)
        len4 = len(descriptionlist)
        if len1 != len2 or len2 != len3 or len3 != len4 or len4 != len1:
            return render(request, "create_competition.html", {'msg': "填写格式出错"})
        rootcompetition = RootCompetition.objects.create(
                                                         name=rootname,
                                                         description=description,
                                                         maxmember=maxmember,
                                                         totalStageNum=len1
                                                         )
        rootcompetition.organizer = userlogin
        rootcompetition.img = newimage
        rootcompetition.save()
        nid = rootcompetition.id
        for i in range(0, len1):
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
    username = request.session['username']
    usertype = request.session['type']
    if request.method == 'GET':
        user = UserLogin.objects.get(username=username)
        id = request.GET['id']
        comp = RootCompetition.objects.get(id=id)
        child_comp = ChildCompetition.objects.filter(root_id=id)
        child_comp_list = []
        for child in child_comp:
            child_comp_list.append({
                'name': child.name,
                'startDate': child.startDate,
                'endDate': child.endDate,
                'description': child.description
            })
        if usertype == 'competitor':
            ismember = bool(comp.members.filter(username=username))
            teamlist = comp.comp.all()
            inteam = False
            for team in teamlist:
                if team.members.filter(username=username):
                    inteam = True
            comp_dict = {
                'isMember': ismember,
                'inTeam': inteam,
                'id': id,
                'name': comp.name,
                'img': comp.img,
                'organizer': comp.organizer.username,
                'totalStageNum': comp.totalStageNum,
                'description': comp.description,
                'maxmember': comp.maxmember,
                'childcompetitionlist': child_comp_list
            }
            return render(request, "competition.html", {'competition': comp_dict})
        elif usertype == 'organizer':
            isorganizer = bool(comp.organizer == user)
            comp_dict = {
                'isOrganizer': isorganizer,
                'id': id,
                'name': comp.name,
                'img': comp.img,
                'organizer': comp.organizer.username,
                'totalStageNum': comp.totalStageNum,
                'description': comp.description,
                'maxmember': comp.maxmember,
                'childcompetitionlist': child_comp_list
            }
            judge_list = []
            judges = user.creator.all()
            for judge in judges:
                name = judge.userlogin.username
                judge_brief_info = {
                    'username': name,
                    'status': bool(comp.judge.filter(username=name))
                }
                judge_list.append(judge_brief_info)
            return render(request, "competition.html", {'competition': comp_dict, 'judgelist': judge_list})
        elif usertype == 'judge':
            isjudge = bool(comp.judge.filter(username=username))
            comp_dict = {
                'isJudge': isjudge,
                'id': id,
                'name': comp.name,
                'img': comp.img,
                'organizer': comp.organizer.username,
                'totalStageNum': comp.totalStageNum,
                'description': comp.description,
                'maxmember': comp.maxmember,
                'childcompetitionlist': child_comp_list
            }
            return render(request, "competition.html", {'competition': comp_dict})
    if request.method == 'POST':
        if usertype == 'competitor':
            name = request.session['username']
            user = UserLogin.objects.get(username=name)
            comp_id = request.POST.get('comp_id')
            comp = RootCompetition.objects.get(id=comp_id)
            comp.members.add(user)
            return redirect('/competition/?id=%s' % comp_id)


@login_required
def createTeam(request):
    if request.method == 'POST':
        name = request.session['username']
        user = UserLogin.objects.get(username=name)
        comp_id = request.POST.get('comp_id')
        comp = RootCompetition.objects.get(id=comp_id)
        team = Team.objects.create(leader=user, name=name+"小队", comp=comp)
        team.members.add(user)
        return redirect('/team/?id=%s' % team.id)


@login_required
def team_info(request):
    if request.method == 'GET':
        id = request.GET['id']
        name = request.session['username']
        team = Team.objects.get(id=id)
        ismember = bool(team.members.filter(username=name))
        isleader = bool(team.leader.username == name)
        members = team.members.all()
        memberlist = []
        for member in members:
            memberlist.append({
                'name': member.username,
            })
        team_dict = {
            'isMember': ismember,
            'isLeader': isleader,
            'id': id,
            'name': team.name,
            'leader': team.leader.username,
            'competition': team.comp.name,
            'memberlist': memberlist
        }
        return render(request, "team.html", {'team': team_dict, 'msg': ''})
    if request.method == 'POST':
        name = request.session['username']
        user = UserLogin.objects.get(username=name)
        team_name = request.POST['name']
        team_id = request.POST['team_id']
        team = Team.objects.get(id=team_id)
        team.name = team_name
        team.save()
        return redirect('/team/?id=%s' % team_id)


@login_required
def team_invite(request):
    if request.method == 'POST':
        team_id = request.POST['team_id']
        name = request.session['username']
        invited_name = request.POST['invited_name']
        team = Team.objects.get(id=team_id)
        user = UserLogin.objects.get(username=name)
        if UserLogin.objects.filter(username=invited_name):
            invited_user = UserLogin.objects.get(username=invited_name)
            if invited_user.type == 'competitor':
                if team.members.filter(username=invited_name):
                    msg = '已在队内'
                else:
                    team.members.add(invited_user)
                    msg = '邀请成功'
            else:
                msg = '无此学生用户'
        else:
            msg = '无此学生用户'
        ismember = bool(team.members.filter(username=name))
        isleader = bool(team.leader.username == name)
        members = team.members.all()
        memberlist = []
        for member in members:
            memberlist.append({
                'name': member.username,
            })
        team_dict = {
            'isMember': ismember,
            'isLeader': isleader,
            'id': team_id,
            'name': team.name,
            'leader': team.leader.username,
            'competition': team.comp.name,
            'memberlist': memberlist
        }
        return render(request, "team.html", {'team': team_dict, 'msg': msg})


@login_required
def organizer_trust(request):
    if request.method == 'POST':
        user_type = request.session['type']
        username = request.session['username']
        comp_id = request.POST.get('comp_id')
        if user_type == 'organizer':
            user = UserLogin.objects.get(username=username)
            comp = RootCompetition.objects.get(id=comp_id)
            judgename = request.POST['checked']
            judge = UserLogin.objects.get(username=judgename)
            judgeinfo = JudgeInfo.objects.get(userlogin=judge)
            if judgeinfo.creator == user and comp.organizer == user:
                comp.judge.add(judge)
        return redirect('/competition/?id=%s' % comp_id)

@login_required
def organizer_cancel(request):
    if request.method == 'POST':
        user_type = request.session['type']
        username = request.session['username']
        comp_id = request.POST.get('comp_id')
        if user_type == 'organizer':
            user = UserLogin.objects.get(username=username)
            comp = RootCompetition.objects.get(id=comp_id)
            judgename = request.POST['checked']
            judge = UserLogin.objects.get(username=judgename)
            judgeinfo = JudgeInfo.objects.get(userlogin=judge)
            if judgeinfo.creator == user and comp.organizer == user:
                comp.judge.remove(judge)
        return redirect('/competition/?id=%s' % comp_id)


@login_required
def file_upload(request):
    if request.method == 'POST':
        user_type = request.session['type']
        username = request.session['username']
        comp_id = request.POST.get('comp_id')
        if user_type == 'competitor':
            newfile = File.objects.create(
                file=request.FILES.get('rootfile'),
                username=username
            )
            newfile.save()
            comp = RootCompetition.objects.get(id=comp_id)
            comp.file.add(newfile)
            comp.save()
        return redirect('/competition/?id=%s' % comp_id)


@login_required
def scoring(request):
    user_type = request.session['type']
    username = request.session['username']
    if request.method == 'GET':
        if user_type == 'judge':
            id = request.GET['id']
            comp = RootCompetition.objects.get(id=id)
            if comp.judge.filter(username=username):
                filelist = comp.file.all()
                return render(request, 'scoring.html', {'filelist': filelist, 'comp_id': id})
        return render('scoring.html')
    if request.method == 'POST':
        comp_id = request.POST.get('comp_id')
        file_id = request.POST.get('file_id')
        if user_type == 'judge':
            comp = RootCompetition.objects.get(id=comp_id)
            file = File.objects.get(id=file_id)
            if comp.judge.filter(username=username):
                file.score = request.POST.get('score')
                file.save()
        return redirect('/scoring/?id=%s' % comp_id)

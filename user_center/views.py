from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse
from login.models import UserLogin
from register.models import CompetitorInfo, OrganizerInfo, JudgeInfo
from django.contrib.auth.models import User
import hashlib
from django.db.models import Q

def hash_code(s, salt='mysite'):  # 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

# Create your views here.
@login_required
def myInfo(request):
    user_type = request.session['type']
    if user_type == 'organizer':
        if request.method == "GET":
            name = request.session['username']
            if OrganizerInfo.objects.filter(name=name):
                organizer = OrganizerInfo.objects.filter(name=name).first()
                name = organizer.name
                email = organizer.email
                status = organizer.authenticationstatus
            else:
                name = ""
                email = ""
                status = 0
            return render(request, "user_center_info_organizer.html", {
                'username': name,
                'email': email,
                'authstatus': status,
            })
        if request.method == "POST":
            name = request.session['username']
            username = request.POST['Username']
            email = request.POST['Email']
            userlogin = UserLogin.objects.get(username=name)
            if OrganizerInfo.objects.filter(userlogin=userlogin):
                competitor = OrganizerInfo.objects.filter(userlogin=userlogin).first()
                competitor.name = username
                competitor.email = email
                competitor.save()
            else:
                competitor = OrganizerInfo.objects.create(name=username,
                                                          email=email,
                                                          userlogin=userlogin,
                                                          )
            return render(request, "user_center_competition_organizer.html", {
                'username': username,
                'email': email,
            })
    elif user_type == 'competitor':
        if request.method == "GET":
            userlogin=UserLogin.objects.get(username=request.session['username'])
            if CompetitorInfo.objects.filter(userlogin=userlogin):
                competitor = CompetitorInfo.objects.filter(userlogin=userlogin).first()
                name = competitor.name
                email = competitor.email
                school = competitor.school
                studentnumber = competitor.studentnumber
                grade = competitor.grade
            else:
                name = ""
                email = ""
                school = ""
                studentnumber = ""
                grade = ""
            return render(request, "user_center_info_competitor.html", {
                'username': name,
                'studentnumber': studentnumber,
                'school': school,
                'grade': grade,
                'email': email
            })
        if request.method == "POST":
            name = request.session['username']
            username = request.POST['Username']
            studentnumber = request.POST['Studentnumber']
            school = request.POST['School']
            email = request.POST['Email']
            grade = request.POST['Grade']
            userlogin = UserLogin.objects.get(username=name)
            if CompetitorInfo.objects.filter(userlogin=userlogin):
                competitor = CompetitorInfo.objects.filter(userlogin=userlogin).first()
                competitor.name = username
                competitor.email = email
                competitor.grade = grade
                competitor.school = school
                competitor.studentnumber = studentnumber
                competitor.save()
            else:
                competitor = CompetitorInfo.objects.create(name=username,
                                                           email=email,
                                                           grade=grade,
                                                           school=school,
                                                           studentnumber=studentnumber,
                                                           userlogin=userlogin,
                                                           )
            return render(request, "user_center_info_competitor.html", {
                'username': username,
                'studentnumber': studentnumber,
                'school': school,
                'grade': grade,
                'email': email,
            })
    elif user_type == 'judge':
        resp = {'errorcode': 1, 'msg': 'no permission'}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        resp = {'errorcode': 1, 'msg': 'no permission'}
        return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def competitor_info(request):
    if request.method == 'GET':
        user_type = request.session['type']
        if user_type != 'C':
            resp = {'errorcode': 1, 'msg': 'no permission'}
            return HttpResponse(json.dumps(resp), content_type="application/json")
        if request.method == 'GET':
            usn = request.user.username
            try:
                user = OrganizerInfo.objects.get(name = usn)
            except:
                return render(request, 'user_center_info_competitor.html',
                              {
                                  'errorcode': 1,
                                  'msg': 'User not found.',
                              })
            info = dict()
            info['email'] = user.email
            info['username'] = user.name
            return render(request, 'user_center_info_competitor.html',
                              {
                                  'errorcode': 0,
                                  'info': info,
                                  'msg': 'Success.',
                              })

@login_required
def organizer_info(request):
    if request.method == 'GET':
        usn = request.user.username
        try:
            user = OrganizerInfo.objects.get(name = usn)
        except:
            return render(request, 'user_center_info_organizer.html', {'msg': 'User not found.'})
        info = dict()
        info['email'] = user.email
        info['username'] = user.name
        return render(request, 'user_center_info_organizer.html')

@login_required
def organizer_auth(request):
    if request.method == 'POST':
        user_type = request.session['type']
        if user_type == 'organizer':
            username = request.session['username']
            organizer = UserLogin.objects.get(username=username)
            organizerinfo = organizer.organizerinfo
            organizerinfo.authenticationstatus = 2
            organizerinfo.save()
            return redirect('/usercenter/myinfo/')

@login_required
def judge_info(request):
    pass


@login_required
def organized_competition_list(request):
    if request.method == 'GET':
        user_type = request.session['type']
        if user_type != 'O':
            resp = {'errorcode': 1, 'msg': 'no permission'}
            return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def candidate_list(request):
    if request.method == 'GET':
        user_type = request.session['type']
        if user_type != 'O':
            resp = {'errorcode': 1, 'msg': 'no permission'}
            return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def myTeam(request):
    team_list = []
    userlogin = UserLogin.objects.get(username=request.session['username'])
    my_team = userlogin.member.all()
    for team in my_team:
        team_info = {
            'id': team.id,
            'name': team.name,
            'leader': team.leader.username,
            'memberlist': team.members.all()
        }
        team_list.append(team_info)
    return render(request, "user_center_team_competitor.html", {
        'teamlist': team_list})

@login_required
def superadmin_adminlist(request):
    if request.method == 'GET':
        user_type = request.session['type']
        if user_type == 'superadmin':
            admin_list = []
            admins = UserLogin.objects.filter(type='admin')
            for admin in admins:
                admin_brief_info = {
                    'username': admin.username,
                }
                admin_list.append(admin_brief_info)
            return render(request, "user_center_adminlist_superadmin.html", {
                'adminlist': admin_list,
            })

@login_required
def superadmin_add_admin(request):
    if request.method == 'POST':
        user_type = request.session['type']
        if user_type == 'superadmin':
            adminname = request.POST['adminname']
            password = request.POST['adminpwd']
            pwd = hash_code(password)
            admin = User.objects.filter(username = adminname)
            if admin.count() > 0:
                return redirect('/usercenter/superadmin/adminlist/')
            User.objects.create_user(username = adminname, password = pwd)
            user_login = UserLogin.objects.create(username = adminname, password = pwd, type = 'admin')
            return redirect('/usercenter/superadmin/adminlist/')

@login_required
def superadmin_delete_admin(request):
    if request.method == 'POST':
        user_type = request.session['type']
        if user_type == 'superadmin':
            adminname = request.POST['adminname']
            User.objects.filter(username = adminname).delete()
            UserLogin.objects.filter(username = adminname).delete()
            return redirect('/usercenter/superadmin/adminlist/')

@login_required
def admin_authlist(request):
    if request.method == 'GET':
        user_type = request.session['type']
        if user_type == 'admin':
            auth_organizer_list = []
            auth_organizers = OrganizerInfo.objects.filter(Q(authenticationstatus=2) | Q(authenticationstatus=3))
            for organizer in auth_organizers:
                organizer_info = {
                    'name': organizer.name,
                    'authstatus': organizer.authenticationstatus,
                }
                auth_organizer_list.append(organizer_info)
            return render(request, "user_center_authlist_admin.html", {
                'authorganizerlist': auth_organizer_list,
            })

@login_required
def admin_authlist_pass(request):
    if request.method == 'POST':
        user_type = request.session['type']
        if user_type == 'admin':
            organizername = request.POST['checked']
            auth_organizer = OrganizerInfo.objects.get(name=organizername)
            auth_organizer.authenticationstatus = 1
            auth_organizer.save()
            return redirect('/usercenter/admin/authlist/')

@login_required
def admin_authlist_deny(request):
    if request.method == 'POST':
        user_type = request.session['type']
        if user_type == 'admin':
            organizername = request.POST['checked']
            auth_organizer = OrganizerInfo.objects.get(name=organizername)
            auth_organizer.authenticationstatus = 3
            auth_organizer.save()
            return redirect('/usercenter/admin/authlist/')


@login_required
def organizer_judgelist(request):
    if request.method == 'GET':
        user_type = request.session['type']
        user = UserLogin.objects.get(username=request.session['username'])
        if user_type == 'organizer':
            judge_list = []
            judges = user.creator.all()
            for judge in judges:
                judge_brief_info = {
                    'username': judge.userlogin.username,
                    'complist': judge.userlogin.juser.all()
                }
                judge_list.append(judge_brief_info)
            return render(request, "user_center_judgelist_organizer.html", {
                'judgelist': judge_list,
            })


@login_required
def organizer_judgelist_add(request):
    if request.method == 'POST':
        user_type = request.session['type']
        user = UserLogin.objects.get(username=request.session['username'])
        if user_type == 'organizer':
            name = request.POST['name']
            password = request.POST['pwd']
            pwd = hash_code(password)
            judge = User.objects.filter(username=name)
            if judge.count() > 0:
                return redirect('/usercenter/judgelist/')
            else:
                user_login = UserLogin.objects.create(username=name, password=pwd, type='judge')
                JudgeInfo.objects.create(userlogin=user_login, creator=user)
                return redirect('/usercenter/judgelist/')

@login_required
def organizer_judgelist_delete(request):
    if request.method == 'POST':
        user_type = request.session['type']
        user = UserLogin.objects.get(username=request.session['username'])
        if user_type == 'organizer':
            name = request.POST['name']
            if UserLogin.objects.filter(username=name):
                if UserLogin.objects.get(username=name).type == 'judge':
                    judge = UserLogin.objects.get(username=name)
                    judgeinfo = JudgeInfo.objects.get(userlogin=judge)
                    if judgeinfo.creator == user:
                        judgeinfo.delete()
                        judge.delete()
            return redirect('/usercenter/judgelist/')

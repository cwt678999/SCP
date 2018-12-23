from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse
from login.models import UserLogin
from register.models import OrganizerInfo,CompetitorInfo
from register.models import CompetitorInfo, OrganizerInfo

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
            else:
                name = ""
                email = ""
            return render(request, "user_center_info_organizer.html", {
                'username': name,
                'email': email
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
            name = request.session['username']
            if CompetitorInfo.objects.filter(name=name):
                competitor = CompetitorInfo.objects.filter(name=name).first()
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



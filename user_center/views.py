from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse
from login.models import UserLogin
from register.models import CompetitorInfo, OrganizerInfo

# Create your views here.

@login_required
def user_center_redirect(request):
    if request.method == 'GET':
        user_type = request.session['type']
        url = ""
        if user_type == 'C':
            url = 'usercenter/competitor/info'
        elif user_type == 'O':
            url = 'usercenter/organizer/info'
        elif user_type == 'J':
            url = 'usercenter/judge/info'
        else:
            resp = {'errorcode': 1, 'msg': 'no permission'}
            return HttpResponse(json.dumps(resp), content_type="application/json")
        resp = {'errorcode': 0, 'url': url, 'msg': 'success'}
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



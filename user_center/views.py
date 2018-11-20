from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from login.models import UserLogin
from register.models import CompetitorInfo, OrganizerInfo

# Create your views here.

@login_required
def info_competitor(request):
    pass

@login_required
def info_organizer(request):
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
def info_judge(request):
    pass

@login_required
def user_center_redirect(request):
    user_type = request.session['type']
    if user_type == 'C':
        info_competitor(request)
    elif user_type == 'O':
        info_organizer(request)
    elif user_type == 'J':
        info_judge(request)

@login_required
def competition_list(request):
    pass
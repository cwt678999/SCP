from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse
from competition_detail.models import CompetitionInfo, CompetitionStageInfo
from register.models import OrganizerInfo

# Create your views here.

@login_required
def competition_list(request):
    if request.method == 'GET':
        comp_list = CompetitionInfo.objects.all()
        resp_list = []
        for comp in comp_list:
            org_id = comp.organizer
            organizer = OrganizerInfo.objects.get(id=org_id)
            first_stage = CompetitionStageInfo.objects.get(competition_id=comp.id, stage_index=1)
            comp_dict = {
                'name': comp.name,
                'organizer': organizer.name
                'start_time': first_stage
            }
    pass
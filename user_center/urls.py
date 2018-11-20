# -*- coding: utf-8 -*-
#

from django.conf.urls import url
from user_center.views import *

__author__ = "Epsirom"

urlpatterns = [
    url(r'^$', user_center_redirect),
    url(r'^organizer/info/?$', competitor_info),
    url(r'^competitor/info/?$', organizer_info),
    url(r'^judge/info/?$', judge_info),
    url(r'^organizer/competition/list?$', organized_competition_list),
    url(r'^organizer/competition/list/candidate/list?$', candidate_list),
]


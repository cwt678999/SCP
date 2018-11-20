# -*- coding: utf-8 -*-
#

from django.conf.urls import url
from user_center.views import *

__author__ = "Epsirom"


urlpatterns = [
    url(r'^/?$', user_center_redirect),
    url(r'^organizer/?$', info_organizer),
    url(r'^competitor/?$', info_competitor),
    url(r'^judge/?$', info_judge),
    url(r'^competition/list?$', competition_list),
]


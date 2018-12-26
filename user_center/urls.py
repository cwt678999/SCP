# -*- coding: utf-8 -*-
#

from django.conf.urls import url
from user_center.views import *

__author__ = "Epsirom"

urlpatterns = [
    #url(r'^$', user_center_redirect),
    url(r'^organizer/info/?$', competitor_info),
    url(r'^organizer/auth/?$', organizer_auth),
    url(r'^competitor/info/?$', organizer_info),
    url(r'^superadmin/adminlist/?$', superadmin_adminlist),
    url(r'^superadmin/adminlist/add/?$', superadmin_add_admin),
    url(r'^superadmin/adminlist/delete/?$', superadmin_delete_admin),
    url(r'^admin/authlist/?$', admin_authlist),
    url(r'^admin/authlist/pass/?$', admin_authlist_pass),
    url(r'^admin/authlist/deny/?$', admin_authlist_deny),
    url(r'^judge/info/?$', judge_info),
    url(r'^organizer/competition/list?$', organized_competition_list),
    url(r'^organizer/competition/list/candidate/list?$', candidate_list),
]


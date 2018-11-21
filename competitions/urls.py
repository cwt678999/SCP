# -*- coding: utf-8 -*-
#

from django.conf.urls import url
from competitions.views import *

__author__ = "Epsirom"

urlpatterns = [
    url(r'^$', competition_list),
]


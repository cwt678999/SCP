"""SCP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from login.views import *
from register.views import *
from competition.views import *
from user_center.views import *
urlpatterns = [
    url(r'^admin/?', admin.site.urls),
    url(r'^login/?', login_view, name="login_url"),
    url(r'^register/?', register),
    url(r'^captcha/?', include('captcha.urls')),
    url(r'^usercenter/?', include('user_center.urls')),
    url(r'^upload/?', include('upload.urls')),
    url(r'^index/?', index_view, name = "home_url"),
    url(r'^create_competition/?', createCompetition, name="create_url"),
    url(r'^usercenter/myinfo/?$', myInfo),
    url(r'^logout?$',logout_view),
    url(r'^usercenter/mycompetition/?', myCompetition),
    url(r'^usercenter/myteam/?', myTeam),
    url(r'^competition/', competition_info),
    url(r'^$',index_view),
]

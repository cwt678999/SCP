from django.db import models
from register.models import OrganizerInfo, CompetitorInfo
from login.models import UserLogin
from upload.models import Image, File
# Create your models here.


class RootCompetition(models.Model):
    organizer = models.ForeignKey(UserLogin, null=True)
    img = models.ForeignKey(File, null=True)
    #file = models.ManyToManyField(File)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=1000)
    totalStageNum = models.IntegerField(default=1)
    members = models.ManyToManyField(UserLogin, related_name='cuser')
    maxmember = models.IntegerField(default=1)


class ChildCompetition(models.Model):
    root_id = models.IntegerField()
    name = models.CharField(max_length=20)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    description = models.CharField(max_length=1000)


class Team(models.Model):
    leader = models.ForeignKey(UserLogin, related_name='leader')
    name = models.CharField(max_length=20)
    members = models.ManyToManyField(UserLogin, related_name='member')
    comp = models.ForeignKey(RootCompetition, null=True, related_name='comp')

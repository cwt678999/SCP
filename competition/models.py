from django.db import models
from register.models import OrganizerInfo,CompetitorInfo
from login.models import UserLogin
from upload.models import Image,File
# Create your models here.
class RootCompetition(models.Model):
    organizer = models.ManyToManyField(UserLogin, related_name='ouser')
    img = models.ManyToManyField(Image)
    #file = models.ManyToManyField(File)
    name = models.CharField(max_length = 20)
    description = models.CharField(max_length = 1000)
    totalStageNum = models.IntegerField()
    members = models.ManyToManyField(UserLogin, related_name='cuser')


class ChildCompetition(models.Model):
    root_id = models.IntegerField()
    name = models.CharField(max_length = 20)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    description = models.CharField(max_length=1000)
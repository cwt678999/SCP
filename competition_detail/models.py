from django.db import models
from register.models import OrganizerInfo
from upload.models import Image

# Create your models here.

class CompetitionInfo(models.Model):
    name = models.CharField(max_length = 100)
    organizer = models.ForeignKey(OrganizerInfo, to_field='id', default=1)
    create_date = models.DateTimeField(auto_now_add=True)
    stage_number = models.IntegerField(default=1)
    description = models.CharField(max_length=1000)
    image = models.ForeignKey(Image, to_field='image')

class CompetitionStageInfo(models.Model):
    competition_id = models.ForeignKey(CompetitionInfo, to_field='id')
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    stage_index = models.IntegerField(default=1)
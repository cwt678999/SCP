from django.db import models
from login.models import UserLogin
# Create your models here.
class CompetitorInfo(models.Model):
    name = models.CharField(max_length=10)
    userlogin = models.OneToOneField(UserLogin)
    email = models.EmailField()
    school = models.CharField(max_length=100)
    studentnumber = models.IntegerField()
    grade = models.CharField(max_length=10)
    gradeid = models.IntegerField()

class OrganizerInfo(models.Model):
    userlogin = models.OneToOneField(UserLogin)
    email = models.EmailField()
    name = models.CharField(max_length = 100)


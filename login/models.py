from django.db import models

# Create your models here.
class UserLogin(models.Model):
    username = models.CharField()
    password = models.CharField()

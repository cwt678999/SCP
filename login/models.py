from django.db import models

# Create your models here.
class UserLogin(models.Model):
    username = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
    type = models.CharField(max_length = 100)
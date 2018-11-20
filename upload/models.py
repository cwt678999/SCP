from django.db import models
from SCP import settings
def getimgpath(instance,filename):
    return '/'.join([MEDIA_ROOT,"img",instance.username,filename])

def getfilepath(instance,filename):
    return '/'.join([MEDIA_ROOT,"file",instance.username,filename])

class Image(models.Model):
    image = models.ImageField(upload_to=getimgpath)
    username = models.CharField(max_length = 20)


class File(models.Model):
    file = models.FileField(upload_to=getfilepath)
    username = models.CharField(max_length = 20)
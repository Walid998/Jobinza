from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from company.models import CreatePost
# Create your models here.


class Profile(models.Model):
    #image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    phonenumber = models.CharField(max_length=50, null=False, blank=True)
    address = models.CharField(max_length=50, null=False, blank=True)
    author 	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class upload(models.Model):
    author 	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  #  job = models.ForeignKey('CreatePost' , on_delete=models.CASCADE ) #job_id
    pdf = models.FileField(upload_to='media/pdfs/')
    status = models.CharField(max_length=30 , default="pending")
  #  cover = models.ImageField(upload_to='media/covers/', null=True, blank=True)

class contacts(models.Model):
    fullname 		= models.CharField(max_length=50, null=False, blank=True)
    email 		= models.CharField(max_length=50, null=False, blank=True)
    phone = models.PositiveIntegerField(null=False, blank=True)
    message 		= models.CharField(max_length=200, null=False, blank=True)

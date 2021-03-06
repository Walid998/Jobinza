from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

class upload(models.Model):
    author 	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='media/pdfs/')
    status = models.CharField(max_length=30 , default="pending")
  #  cover = models.ImageField(upload_to='media/covers/', null=True, blank=True)

class contacts(models.Model):
    fullname 		= models.CharField(max_length=50, null=False, blank=True)
    email 		= models.CharField(max_length=50, null=False, blank=True)
    phone =   models.PositiveIntegerField(null=False, blank=True)
    message 		= models.CharField(max_length=200, null=False, blank=True)

class Resume_Parsed(models.Model):
    usrname       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name          = models.CharField('Name', max_length=255, null=True, blank=True)
    email         = models.CharField('Email', max_length=255, null=True, blank=True)
    mobile_number = models.CharField('Mobile Number',  max_length=255, null=True, blank=True)
    education     = models.CharField('Education', max_length=255, null=True, blank=True)
    skills        = models.CharField('Skills', max_length=1000, null=True, blank=True)
    company_name  = models.CharField('Company Name', max_length=1000, null=True, blank=True)
    college_name  = models.CharField('College Name', max_length=1000, null=True, blank=True)
    designation   = models.CharField('Designation', max_length=1000, null=True, blank=True)
    experience    = models.CharField('Experience', max_length=1000, null=True, blank=True)
    uploaded_on   = models.DateTimeField('Uploaded On', auto_now_add=True)
    total_experience  = models.CharField('Total Experience (in Years)', max_length=1000, null=True, blank=True)

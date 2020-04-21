from django.db import models
from django.contrib.auth.models import User
from django.conf import settings



def upload_location(instance, filename, **kwargs):
	file_path = 'profile-pic/applicant/{author_id}/{filename}'.format(
			author_id=str(instance.author), filename=filename
		) 
	return file_path


class Profile(models.Model):
    resume        = models.FileField('Upload Resumes', upload_to='resumes/')
    image = models.ImageField('image',upload_to= upload_location, null=False, blank=True)    
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    phonenumber = models.CharField(max_length=50, null=False, blank=True)
    address = models.CharField(max_length=100, null=False, blank=True)
    location = models.CharField(max_length=50, null=False, blank=True)
    description = models.CharField(max_length=500, null=False, blank=True)
    author 	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
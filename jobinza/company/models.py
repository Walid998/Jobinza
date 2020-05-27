from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from datetime import datetime , date
from django.urls import reverse
from django.contrib.auth.models import User

def upload_location(instance, filename, **kwargs):
	file_path = 'company/{author_id}/{jobtitle}-{filename}'.format(
			author_id=str(instance.author), jobtitle=str(instance.jobtitle), filename=filename
		) 
	return file_path


class CreatePost(models.Model):
    
    jobtitle 		= models.CharField(max_length=50, null=False, blank=True)
    job_description 	= models.CharField(max_length=500, null=False, blank=True)
    joblocation             = models.CharField(max_length=50, null=False, blank=True)
    city     		= models.CharField(max_length=50, null=False, blank=True)
    Area    		= models.CharField(max_length=50, null=False, blank=True)
    careerlevel 		= models.CharField(max_length=50, null=False, blank=True)
    year_of_experience 	= models.CharField(max_length=50, null=False, blank=True)
    salary_range1 		= models.CharField(max_length=50, null=False, blank=True)  
    salary_range2 		= models.CharField(max_length=50, null=False, blank=True)
    num_vacancies 		= models.TextField(max_length=50, null=False, blank=True)
    #rolejob 		= models.ForeignKey('jobRole' , on_delete=models.CASCADE)
    #related_industry 	= models.ForeignKey('relatedIndustry' , on_delete=models.CASCADE)
    jobtype			= models.CharField(max_length=50, null=False, blank=True)
    #skills 			= models.ForeignKey('skills' , on_delete=models.CASCADE )
    image 				= models.ImageField(upload_to=upload_location, null=False, blank=True)
    skills 			= models.CharField(max_length=500, null=False, blank=True)
    deadline 		= models.DateField(null=False, blank=True ) 
    status          = models.CharField(max_length=10 , default="Publishing" )
    category        = models.ForeignKey('category' , on_delete = models.CASCADE)
    date_published 		= models.DateTimeField(auto_now_add=True, verbose_name="date published")
    date_updated 		= models.DateTimeField(auto_now=True, verbose_name="date updated")
    author 			= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug 			= models.SlugField(blank=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.jobtitle
    
    def get_absolute_url(self):
        return  reverse('details',args=[self.pk])


class Match_Results(models.Model):
    resume = models.CharField('resume', max_length=100, null=True, blank=True)
    aplcnt = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    app_email = models.CharField('email',max_length=50, null=False, blank=True)
    job_id = models.IntegerField('the job', null=True, blank=True)
    skills_rslt = models.FloatField('match result', max_length=1000, null=True, blank=True)
    status = models.CharField('status', max_length=100, null=True, blank=True)
    content = models.CharField(max_length=300,null=True,blank=True)
    def __str__(self):
        return self.id

class Send_Email(models.Model):
    username = models.CharField(max_length=50 , null=True , blank = True)
    email = models.EmailField(max_length=50 , null=True , blank = True)
    content = models.CharField(max_length=350 , null=True , blank = True)
# class jobRole(models.Model):
#     name = models.CharField(max_length = 50 , primary_key=True)

# class relatedIndustry(models.Model):
#     name = models.CharField(max_length = 50 , primary_key=True)

# class skills(models.Model):
#     name = models.CharField(max_length = 70 , primary_key=True)


###
#@receiver(post_delete, sender=CreatePost)
#def submission_delete(sender, instance, **kwargs):
#	instance.image.delete(False)

#def pre_save_job_post_receiever(sender, instance, *args, **kwargs):
#	if not instance.slug:
#		instance.slug = slugify(instance.author.username + "-" + instance.jobtitle)

#pre_save.connect(pre_save_job_post_receiever, sender=CreatePost)

class Notification(models.Model):
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    verb = models.CharField(max_length=100 , null= False)
    description = models.TextField()
    read = models.BooleanField(default=False)
    post = models.IntegerField()
    applicant = models.IntegerField()

class category(models.Model):
    name = models.CharField( max_length=100 ,primary_key=True)
    jobno = models.IntegerField(null=True,blank=True)
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from django.utils import timezone



def upload_location(instance, filename, **kwargs):
	file_path = 'company/{author_id}/{company_name}-{filename}'.format(
			author_id=str(instance.author.id), company_name=str(instance.company_name), filename=filename
		) 
	return file_path


class CreatePost(models.Model):
    company_name 		= models.CharField(max_length=50, null=False, blank=True)
    jobtitle 		= models.CharField(max_length=50, null=False, blank=True)
    joblocation             = models.CharField(max_length=50, null=False, blank=True)
    city     		= models.CharField(max_length=50, null=False, blank=True)
    Area    		= models.CharField(max_length=50, null=False, blank=True)
    careerlevel 		= models.CharField(max_length=50, null=False, blank=True)
    year_of_experience 	= models.CharField(max_length=50, null=False, blank=True)
    salary_range 		= models.CharField(max_length=50, null=False, blank=True)
    additional_salary 	= models.CharField(max_length=50, null=False, blank=True)
    num_vacancies 		= models.TextField(max_length=50, null=False, blank=True)
    rolejob 		= models.CharField(max_length=50, null=False, blank=True)
    related_industry 	= models.CharField(max_length=50, null=False, blank=True)
    jobtype			= models.CharField(max_length=50, null=False, blank=True)
    job_description 	= models.CharField(max_length=500, null=False, blank=True)
    skills 			= models.CharField(max_length=500, null=False, blank=True)
    image 			= models.ImageField(upload_to=upload_location, null=False, blank=True)
    date_published 		= models.DateTimeField(auto_now_add=True, verbose_name="date published")
    date_updated 		= models.DateTimeField(auto_now=True, verbose_name="date updated")
    author 			= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug 			= models.SlugField(blank=True, unique=True)



@receiver(post_delete, sender=CreatePost)
def submission_delete(sender, instance, **kwargs):
	instance.image.delete(False)

def pre_save_job_post_receiever(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.author.username + "-" + instance.company_name)

pre_save.connect(pre_save_job_post_receiever, sender=CreatePost)


class Listshow(models.Model):
    jobtitle 		= models.CharField(max_length=50, null=False, blank=True)
    city = models.TextField()
    area = models.TextField()
    post_date = models.DateTimeField(default=timezone.now)
    post_update = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    def __str__(self):
        return self.jobtitle


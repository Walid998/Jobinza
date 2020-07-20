#from django.urls import path 
#from . import views

#urlpatterns = [
#    path('', views.home, name='home'),
#]

from django.urls import path
from . import views

app_name = 'applicant'

urlpatterns = [
#	path('details/', views.job_details, name="job_details"),
	path('details/<int:job_id>/', views.job_details, name='emp_detail'),
	path('profile/<str:user_name>/', views.profile_info, name='profile'),
	path('',views.editProfile, name='edit-profile'),
	path('uploadresume/<str:jbid>',views.uploadResume,name='uploadResume'),
	path('applyforjob/<str:jbid>',views.ApplyForJob,name='ApplyForJob'),
	path('listapp/',views.list_applicant,name='list_app'),
	path('applied_jobs/',views.applied_jobs,name='listapp'),
	path('indeed/',views.showResult , name='indeed'),
	path('home/',views.home_applicant,name='home_applicant'),
	#path('about/',views.about,name='about')
	#path('details/', views.job_details, name='emp_detail'),
]
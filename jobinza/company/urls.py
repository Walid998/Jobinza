#from django.urls import path 
#from . import views

#urlpatterns = [
#    path('', views.home, name='home'),
#]

from django.urls import path
from company.views import create_post_view	
from company.views import list_job_view ,addjobRole_view ,addRelatedIndustry_view ,addskill_view

app_name = 'company'

urlpatterns = [
	path('create/', create_post_view, name="create"),
	path('list/' , list_job_view , name="list"),
	path('role/' , addjobRole_view , name="jobRole"),
	path('industry/' , addRelatedIndustry_view , name="industry"),
	path('skills/' , addskill_view , name="skills"),
	#path('<slug>/', detail_post_view, name="detail"),
	#path('<slug>/edit', edit_post_view, name="edit"),
]
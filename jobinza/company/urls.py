#from django.urls import path 
#from . import views

#urlpatterns = [
#    path('', views.home, name='home'),
#]

from django.urls import path
from company.views import create_post_view	
from company.views import (
	list_job_view ,
	addjobRole_view ,
	job_delete,
	addRelatedIndustry_view ,
	addskill_view,
	job_state_closed,
	PostDeleteView,
	job_edit,
	job_details,
	PostUpdateView)


app_name = 'company'

urlpatterns = [
	path('create/', create_post_view, name="create"),
	path('list/' , list_job_view , name="list"),
	path('role/' , addjobRole_view , name="jobRole"),
	path('industry/' , addRelatedIndustry_view , name="industry"),
	
	path('skills/' , addskill_view , name="skills"),
	path('delete/<int:job_id>/' ,job_delete,name='delete'),
	path('details/<int:job_id>/', job_details, name='detials'),
	path('edit/<int:job_id>/', job_edit, name='edit'),
	path('status/<int:job_id>/',job_state_closed),
	
	path('list/<slug:pk>/update/', PostUpdateView.as_view(), name='edit'),
	path('list/<slug:pk>/delete/',PostDeleteView.as_view(), name='delete'),
	#path('<slug>/', detail_post_view, name="detail"),
	#path('<slug>/edit', edit_post_view, name="edit"),
]
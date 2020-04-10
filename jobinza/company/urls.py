#from django.urls import path 
#from . import views

#urlpatterns = [
#    path('', views.home, name='home'),
#]

from django.urls import path
from company.views import create_post_view	
from company.views import (
	list_job_view ,
	job_delete,
	job_state_closed,
	job_state_open,
	job_edit,
	job_details,
	list_job_close_view,
	list_job_publish_view,
	send_email,
	read_notification,
	profile_info,
	editProfile,
	
 )


app_name = 'company'

urlpatterns = [
	path('create/', create_post_view, name="create"),
	path('list/' , list_job_view , name="list"),
	path('delete/<int:job_id>/' ,job_delete,name='delete'),
	path('details/<int:job_id>/', job_details, name='detials'),
	path('edit/<int:job_id>/', job_edit, name='edit'),
	path('status/<int:job_id>/',job_state_closed),
	path('status_open/<int:job_id>',job_state_open),
	path('list_close/' , list_job_close_view , name="list"),
	path('list_publish/' , list_job_publish_view , name="list"),
	path('send_email/' ,send_email,name="send_email"),
	path('profile/<str:user_name>/', profile_info, name='profile'),
	path('',editProfile, name='edit-profile'),
	#path('<slug>/', detail_post_view, name="detail"),
	#path('<slug>/edit', edit_post_view, name="edit"),
	path('notification/' , read_notification , name="notification"),

]
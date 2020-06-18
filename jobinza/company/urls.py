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
	send_email,
	readall_notification,
	profile_info,
	editProfile,
	category_posts,
	status_accepted,
	status_rejected,
 )


app_name = 'company'

urlpatterns = [
	
	path('create/', create_post_view, name="create"),
	path('list/' , list_job_view , name="list"),
	path('delete/<int:job_id>/' ,job_delete,name='delete'),
	path('details/<str:user_name>/<int:job_id>/', job_details, name='detials'),
	path('edit/<int:job_id>/', job_edit, name='edit'),
	path('status/<int:job_id>/',job_state_closed),
	path('status_open/<int:job_id>',job_state_open),
	path('status_accepted/<int:pk>/',status_accepted),
	path('Rejected/<int:pk>/',status_rejected),
	path('send_email/<str:user_name>/<int:job_id>/',send_email,name="send_email"),
	path('profile/<str:user_name>/', profile_info, name='profile'),
	path('edit_pro/<str:user_name>/',editProfile, name='edit_pro'),
	#path('<slug>/', detail_post_view, name="detail"),
	#path('<slug>/edit', edit_post_view, name="edit"),
	path('read_notification/' , readall_notification , name="notification"),
	path('catgeory_posts/<str:category_name>' , category_posts , name="categoryPosts"),


]
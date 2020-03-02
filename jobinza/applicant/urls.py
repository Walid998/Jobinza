#from django.urls import path 
#from . import views

#urlpatterns = [
#    path('', views.home, name='home'),
#]

from django.urls import path
from . import views

app_name = 'applicant'

urlpatterns = [
	path('details/', views.job_details, name="job_details"),
]
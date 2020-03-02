from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from company import views

from account.views import (
    registration_view_hr,    
    registration_view,
    logout_view,
    login_view,
    #account_view,
    #must_authenticate_view,
    home,
)


urlpatterns = [
    #path('', views.home, name='home'),
    path('',home,name='home'),
    path('company/', include('company.urls', 'post')),
    path('admin/', admin.site.urls),
    #path('account/', account_view, name="account"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    #path('must_authenticate/', must_authenticate_view, name="must_authenticate"),
    path('signup/', registration_view, name="signup"),
    path('signup/hr/' , registration_view_hr , name="register"),
	path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
     name='password_reset_complete'),


    path('account/', include('account.urls')), 

]

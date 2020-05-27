from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from applicant.views import contact,search
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from account.views import (
    registration_view_hr,    
    registration_view,
    logout_view,
    login_view,
    guestPage,
    account_setting,
    #account_view,
    #must_authenticate_view,
)


urlpatterns = [
    #path('', views.home, name='home'),
    path('',guestPage,name='home'),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('company/', include('company.urls', 'post')),
    path('admin/', admin.site.urls),
    #path('account/', account_view, name="account"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    #path('must_authenticate/', must_authenticate_view, name="must_authenticate"),
    path('signup/', registration_view, name="signup"),
    path('contact/',contact, name='contact'),
    
    path('signup/hr/' , registration_view_hr , name="register"),
	path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='account/password_change.html'), 
        name='password_change'),
    
    path('account_setting/<int:user_id>/', account_setting, name='account_setting'),
        path('reset-password', PasswordResetView.as_view(), name='password_reset'),
    path('reset-password/done', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset-password/confirm/<uidb64>[0-9A-Za-z]+)-<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password/complete/',PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    url(r'^search/$',search,name="search"),

    path('applicant/', include('applicant.urls')), 

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
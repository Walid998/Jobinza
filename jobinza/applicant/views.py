from django.shortcuts import render
from company.models import CreatePost
from applicant.models import Profile
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from company.views import update_status
# Create your views here.


def job_details(request , job_id):
    job =None
    id_num = int(job_id)
    job_list = CreatePost.objects.get(id=id_num)

    return render(request,'applicant/job_details.html', {'job': job_list})

@login_required(login_url='login')
def home(request):
    update_status()
    listpost=CreatePost.objects.all()
    context={
        'title':'home',
        'posts':listpost
    }
    return render(request,'applicant/home.html',context)


@login_required(login_url='login')
def profile_info(request):
    """ info = Profile.objects.all()
    context={
        'title':'profile',
        'info':info
    } """
    return render(request,'applicant/profile.html')

from django.shortcuts import render
from company.models import CreatePost
from applicant.models import Profile
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from company.views import update_status
from django.contrib.auth.models import User

# Create your views here.

@login_required(login_url='login')
def job_details(request , job_id):
    id_num = int(job_id)
    job_list = CreatePost.objects.get(id=id_num)

    return render(request,'applicant/job_details.html', {'job': job_list})


def home(request):
    
    return render(request,'applicant/guest.html')

def contact(request):
    
    return render(request,'applicant/contact.html')


@login_required(login_url='login')
def profile_info(request,user_name):
    user_info = User.objects.get(username=user_name)
    pk = User.objects.get(username=user_name).pk
    try:
        profile_info = Profile.objects.get(author = pk)
       # context['title']='profile',
        return render(request,'applicant/profile.html', {'result': user_info , 'info':profile_info } )
    except:
        return render(request,'applicant/profile.html', {'result': user_info , 'info':'' })

def addinfo (request):
    user = request.user
    if request.method == 'POST':
        author = User.objects.filter(username=user.username).first()
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ',author)
        job = Profile()
        job.phonenumber = request.POST.get('phone')
        job.address = request.POST.get('address')
        job.author = author
        job.save()
    return render(request, 'applicant/form.html')

@login_required(login_url='login')
def list_applicant(request):
    update_status()
    listpost=CreatePost.objects.all()
    context={
        'title':'home',
        'posts':listpost
    }
    return render(request,'applicant/home.html',context)
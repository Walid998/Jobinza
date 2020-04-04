from django.shortcuts import render , redirect
from company.models import CreatePost
from applicant.models import Profile
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from company.views import update_status
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from applicant.forms import uploadForm
from applicant.models import contacts,Resume_Parsed
from applicant.forms import contactform
from applicant.forms import editprofileForm
from django.conf import settings
from pyresparser import ResumeParser
import os
import sys
# Create your views here.

@login_required(login_url='login')
def job_details(request , job_id):
    id_num = int(job_id)
    job_list = CreatePost.objects.get(id=id_num)

    return render(request,'applicant/job_details.html', {'job': job_list })

def home(request):   
    update_status()
    listusers = User.objects.all()
    listpost=CreatePost.objects.all()

    return render(request,'applicant/guest.html' , {'posts':listpost , 'users': listusers})

def contact(request):
    if request.method =='POST':
            post=contacts()
            post.fullname=request.POST.get('fullname')
            post.email=request.POST.get('email')
            post.phone=request.POST.get('phone')
            post.message=request.POST.get('message')
            post.save()
            
    
    return render(request,'applicant/contact.html')



@login_required(login_url='login')
def profile_info(request,user_name):
    user_info = User.objects.get(username=user_name)
    pk = User.objects.get(username=user_name).pk
    try:
        p_info = Profile.objects.get(author = pk)
        return render(request,'applicant/profile.html', {'result': user_info , 'info':p_info } )
    except:
        return render(request,'applicant/profile.html', {'result': user_info , 'info':'' })


@login_required(login_url='login')
def editProfile (request):    
    if request.method == 'POST':
        uname = request.user
        auth = User.objects.get(username=uname)
        pk = User.objects.get(username=uname).pk
        try:
            pinfo = Profile.objects.get(author = pk)
            print("***********<<<<<<< pinfo has data >>>>>>>***********")
            form = editprofileForm(request.POST ,instance = pinfo)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.save()
                #messages.success(request,f'Job has been updated successfully !!')
                return redirect(f'/applicant/profile/{request.user}')
        except:
            form = editprofileForm(request.POST , request.FILES)
            if form.is_valid():
                print("<<< pinfo has no data >>>")
                inst = Profile()
                inst.image = form.cleaned_data.get('image')
                print ('**************************',inst.image)
                inst.phonenumber = form.cleaned_data.get('phonenumber')
                inst.address = form.cleaned_data.get('address')
                inst.author = auth
                inst.save()
                return redirect(f'/applicant/profile/{request.user}')

@login_required(login_url='login')
def list_applicant(request):
    update_status()
    listusers = User.objects.all()
    listpost=CreatePost.objects.all()

    return render(request,'applicant/home.html', {'posts' : listpost , 'users': listusers} )

#####################################
########____UPLOAD RESUME____########
@login_required(login_url='login')
def upload(request):
    if request.method == 'POST':
        user = request.user
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name,uploaded_file)
        # context['url'] = fs.url(name)
        pars=Resume_Parsed()
        parser = ResumeParser(os.path.join(settings.MEDIA_ROOT, uploaded_file.name))
        data = parser.get_extracted_data()
        pars.usrname = user
        pars.resume = uploaded_file
        pars.name = data.get('name')
        pars.email              = data.get('email')
        pars.mobile_number      = data.get('mobile_number')
        if data.get('degree') is not None:
            pars.education      = ', '.join(data.get('degree'))
        else:
            pars.education      = None
        pars.company_names      = data.get('company_names')
        pars.college_name       = data.get('college_name')
        pars.designation        = data.get('designation')
        pars.total_experience   = data.get('total_experience')
        if data.get('skills') is not None:
            pars.skills         = ', '.join(data.get('skills'))
        else:
            pars.skills         = None
        if data.get('experience') is not None:
            pars.experience     = ', '.join(data.get('experience'))
        else:
            pars.experience     = None
        pars.save()
        fs.delete(uploaded_file.name)
        
    return render(request ,'applicant/test_upload.html')
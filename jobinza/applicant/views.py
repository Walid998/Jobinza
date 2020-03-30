from django.shortcuts import render , redirect
from company.models import CreatePost, Match_Results
from applicant.models import Profile
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from company.views import update_status, skillsToList
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from applicant.forms import uploadForm
from applicant.models import contacts,Resume_Parsed
from applicant.forms import contactform
from django.conf import settings
from pyresparser import ResumeParser
from django.contrib import messages
import os
from django.db.models import Q
from django.core.paginator import Paginator
# Create your views here.

def Percent(number,List):
    percent = f'{(number/len(List))*100.00:.2f}'
    return percent

def Comparison(hrSkills,AppSkills):
    found= 0
    for i in hrSkills:
        if i in AppSkills:
            found=found+1
    return Percent(found,hrSkills)

@login_required(login_url='login')
def job_details(request , job_id):
    user = request.user
    job = CreatePost.objects.get(id=job_id)
    state = ''
    prof = ''
    if request.method == 'POST':
        try:
            uploaded_file = request.FILES['cv']
            fs = FileSystemStorage()
            fs.save(uploaded_file.name,uploaded_file)
            try:
                prof =Profile.objects.get(author = user)
                prof.resume = uploaded_file
                prof.save()
            except:
                prof = Profile()
                prof.author = user
                prof.resume = uploaded_file
                prof.save()
            parser_r(uploaded_file,uploaded_file.name,user)
            fs.delete(uploaded_file.name)
            state = 'new'
        except:
            prof = Profile.objects.get(author = user) # profile details
            pars_obj = Resume_Parsed.objects.get(usrname = user)
            match = Match_Results()
            match.resume = prof.resume
            match.author = user
            match.job_id = job.id
            reslt =Comparison(skillsToList(job.skills), skillsToList(pars_obj.skills))
            match.skills_rslt = reslt
            match.status = 'pending'
            match.save()
    context = {
        'skills':skillsToList(job.skills),
        'job': job,
        'user_':prof,
        'newcv': state
    }
    return render(request,'applicant/job_details.html', context)

def home(request):   
    update_status()
    listusers = User.objects.all()
    listpost=CreatePost.objects.all()
    paginator = Paginator(listpost,2)
    page = request.GET.get('page')
    listpost = paginator.get_page(page)
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
        profile_info = Profile.objects.get(author = pk)
       # context['title']='profile',
        return render(request,'applicant/profile.html', {'result': user_info , 'info':profile_info } )
    except:
        return render(request,'applicant/profile.html', {'result': user_info , 'info':'' })

def update (request):
    user = request.user
    if request.method == 'POST':
        """ author = User.objects.filter(username=user.username).first()
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ',author) """
        job = Profile()
        job.phonenumber = request.POST.get('phone')
        job.address = request.POST.get('address')
        job.author = author
        job.save()
    return profile_info()

@login_required(login_url='login')
def list_applicant(request):
    update_status()
    listusers = User.objects.all()
    listpost=CreatePost.objects.all()

    return render(request,'applicant/home.html', {'posts' : listpost , 'users': listusers} )

#####################################
########____UPLOAD RESUME____########
def parser_r(resume,resume_name,user):
    pars=Resume_Parsed()
    parser = ResumeParser(os.path.join(settings.MEDIA_ROOT, resume_name))
    data = parser.get_extracted_data()
    pars.usrname = user
    pars.resume = resume
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

###################search################################

def search(request):
    if request.method=='POST':
        srch = request.POST['srh']

        if srch:
            match = CreatePost.objects.filter(
                Q(jobtitle__icontains=srch)|Q(city__icontains=srch)
            )
            if match:
                return render(request,'applicant/search.html',{'sr':match})
            else:
                messages.error(request,'no result found')
        else:
            return HttpResponseRedirect('/search/')
    return render(request,'applicant/search.html')
from django.shortcuts import render , redirect
from company.models import CreatePost, Match_Results , category
from account.models import Profile
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from company.views import skillsToList , update_status
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from applicant.forms import uploadForm ,contactform
from applicant.models import contacts,Resume_Parsed
from applicant.forms import contactform , SeeJobsForm
from applicant.forms import editprofileForm
from applicant.utils import Comparison 
from django.conf import settings
from pyresparserx import ResumeParser
from django.contrib import messages
from django.http import HttpResponseRedirect
import os
from django.db.models import Q
from django.core.paginator import Paginator
from Jobinza.utils import PaginatorX
from account.decorators import allowed_users , unauthenticated_user
# Create your views here.


@login_required(login_url='login')
def home_applicant(request):
    return render(request,'applicant/home_applicant.html')


#@login_required(login_url='login')
#@allowed_users(allowed_roles=['applicant'])
def job_details(request , job_id):
    user = request.user
    #print('>>>>>>>>>>>>>>>>>> >>  : ',user.email)
    job = CreatePost.objects.get(id=job_id)
    job.views = job.views + 1
    job.save()
    com = User.objects.get(id=job.author_id)
    com_profile = ''
    try:
        com_profile = Profile.objects.get(author_id=com.id)
    except:
        com_profile = ''

    hasResume = False
    isApplied = False
    try:
        user_profile = Profile.objects.get(author = user.id)
        if user_profile.resume != "":
            hasResume = True
        else:
            hasResume = False
    except:
        hasResume = False
    
    try:
        mtch = Match_Results.objects.get(aplcnt = user.id,job_id=job_id)
        if mtch.status == 'pending':
            isApplied = True
    except:
        isApplied = False   

    r = None
    try:
        r = CreatePost.objects.all().filter(category = job.category)
    except:
        print("no jobs in this category") 
    context = {
        'job': job,
        'skills':skillsToList(job.skills),
        'has_resume': hasResume ,
        'company':com ,
        'profile':com_profile ,
        'isapplied':isApplied ,
        'simi_jobs' : r
    }
    return render(request,'applicant/job_details.html', context)

def uploadResume(request,jbid):
    user = request.user
    if request.method == 'POST':
        uploaded_file = request.FILES['cv']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name,uploaded_file)
        parser_r(uploaded_file,uploaded_file.name,user)
        try:
            prof =Profile.objects.get(author = user.id)
            prof.resume = uploaded_file
            prof.save()
        except:
            prof = Profile()
            prof.author = user
            prof.resume = uploaded_file
            prof.save()
        
        fs.delete(uploaded_file.name)
        return redirect(f'/applicant/details/{jbid}')

def ApplyForJob(request,jbid):
    user = request.user
    isApplyed = False
    try:
        test_match = Match_Results.objects.get(aplcnt= user.id,job_id=jbid)
        isApplyed = True
    except:
        isApplyed = False
    if request.method == 'POST' and isApplyed == False:
        print("alppplied")
        prof = Profile.objects.get(author = user) # profile details
        pars_obj = Resume_Parsed.objects.get(usrname = user)
        print("LLLLLLLLLLLL?>>>>>>>>> ",pars_obj)
        job = CreatePost.objects.get(id= jbid)
        match = Match_Results()
        match.resume = prof.resume
        match.aplcnt = user
        print("onetwothree",user)
        match.app_email = user.email
        match.job_id = job.id
        match.company = job.author_id
        print("yyyyyyyyyyyyyyyyyyyyyyyyyyyyy",job.author_id)
        reslt =Comparison(skillsToList(job.skills), skillsToList(pars_obj.skills))
        match.skills_rslt = reslt['percent']
        match.matched_skills = reslt['fnd']
        match.not_matched_skills = reslt['nfnd']
        match.experience = pars_obj.experience
        match.status = 'pending'
        match.save()
        return redirect(f'/applicant/details/{jbid}')
    else:
        return redirect(f'/applicant/details/{jbid}')
        
@unauthenticated_user
def contact(request):
    if request.method =='POST':
        post=contacts()
        post.fullname=request.POST.get('fullname')
        post.email=request.POST.get('email')
        post.phone=request.POST.get('phone')
        post.message=request.POST.get('message')
        post.save()
    return render(request,'applicant/contact.html')
@unauthenticated_user
def about(request):
    return render(request, 'applicant/about.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=[ 'applicant','employeer'])
def profile_info(request,user_name):
    user_info = User.objects.get(username=user_name)
    pk = User.objects.get(username=user_name).pk
    try:
        p_info = Profile.objects.get(author = pk)
        return render(request,'applicant/profile.html', {'result': user_info , 'info':p_info } )
    except:
        return render(request,'applicant/profile.html', {'result': user_info , 'info':'' })


@login_required(login_url='login')
@allowed_users(allowed_roles=['applicant'])
def editProfile (request):    
    if request.method == 'POST':
        print('<><><><><><><>>>>>>>>>>>>>>>>>>>>>> ',request.FILES['image'])
        uname = request.user
        auth = User.objects.get(username=uname)
        pk = User.objects.get(username=uname).pk
        try:
            pinfo = Profile.objects.get(author = pk)
            print("***********<<<<<<< pinfo has data >>>>>>>***********")
            form = editprofileForm(request.POST, request.FILES ,instance = pinfo)
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
                inst.image = request.FILES.get('image')
                print ('**************************',inst.image)
                inst.phonenumber = form.cleaned_data.get('phonenumber')
                inst.address = form.cleaned_data.get('address')
                inst.job_title = form.cleaned_data.get('job_title')
                inst.author = auth
                inst.save()
                return redirect(f'/applicant/profile/{request.user}')

@login_required(login_url='login')
@allowed_users(allowed_roles=['applicant'])
def list_applicant(request):
    update_status(request)
    listusers = User.objects.all()
    listpost=CreatePost.objects.all()
    listpost = PaginatorX(request,listpost,5)
    info = ""
    data = ""
    try:
        info = Profile.objects.get(author_id=request.user.id)
        print("MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM:: ",info)
        t = str(info.job_title)
        z = str(info.address)
        jobsearch = IndeedJobSearch(title=t, location=z)
        data = jobsearch.getJobs()
        datas = Paginator(data,3)
        page = request.GET.get('page')
        data_paginator = datas.get_page(page)
    except:
        info = ""

    context = {
        'posts' : listpost , 
        'users': listusers,
        'data' : data,
        'info' : info,
    }
    return render(request,'applicant/home.html', context )

#####################################
########____UPLOAD RESUME____########
# @login_required(login_url='login')
# @allowed_users(allowed_roles=['applicant'])
def parser_r(resume,resume_name,user):
    pars=Resume_Parsed()
    parser = ResumeParser(os.path.join(settings.MEDIA_ROOT, resume_name))
    data = parser.get_extracted_data()
    pars.usrname = user
    # pars.resume = resume
    pars.name = data.get('name')
    pars.email              = data.get('email')
    pars.mobile_numberF      = data.get('mobile_number')
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
        print('>>>>>>>>>>>>>>>>>>>>> ', srch)
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['applicant'])
def applied_jobs(request):
    posts = []
    result = Match_Results.objects.all().filter(aplcnt = request.user.id)
    for r in result:
        post = CreatePost.objects.get(id = r.job_id)
        posts.append(post)
    users = User.objects.all()
    
    return render (request , 'applicant/applied_jobs.html' , {'result' : result , 'posts': posts , 'users' :users} ) 



    # isNewUser = False
    # prof = ''
    # isApplied = False
    # try:
    #     prof =Profile.objects.get(author = user.id)
    #     if prof.resume == None:
    #         isNewUser = True
    #     else:
    #         isNewUser = False
    # except:
    #     isNewUser = True

    # try:
    #     res = Match_Results.objects.get(aplcnt = user.id,job_id=job_id)
    #     if res.status == 'pending':
    #         isApplied = True
    # except:
    #     print('not apply yet',user.id)

    # context = {
    #     'skills':skillsToList(job.skills),
    #     'job': job,
    #     'isapplied':isApplied,
    #     'newuser': isNewUser
    # }

    # if request.method == 'POST' and user.is_authenticated:
    #     try:
    #         uploaded_file = request.FILES['cv']
    #         fs = FileSystemStorage()
    #         fs.save(uploaded_file.name,uploaded_file)
            
    #         try:
    #             prof =Profile.objects.get(author = user.id)
    #             prof.resume = uploaded_file
    #             prof.save()
    #         except:
    #             prof = Profile()
    #             prof.author = user
    #             prof.resume = uploaded_file
    #             prof.save()
    #         parser_r(uploaded_file,uploaded_file.name,user)
    #         fs.delete(uploaded_file.name)
    #         isNewUser=False
    #         return render(request,'applicant/job_details.html',{'skills':skillsToList(job.skills),'job': job,'isapplied':isApplied,'newuser': isNewUser,'applynow':True} )
    #     except:
    #         prof = Profile.objects.get(author = user) # profile details
    #         pars_obj = Resume_Parsed.objects.get(usrname = user)
    #         if isApplied == False:
    #             match = Match_Results()
    #             match.resume = prof.resume
    #             match.aplcnt = user
    #             match.app_email = user.email
    #             match.job_id = job.id
    #             reslt =Comparison(skillsToList(job.skills), skillsToList(pars_obj.skills))
    #             match.skills_rslt = reslt
    #             match.status = 'pending'
    #             match.save()
    #             return render(request,'applicant/job_details.html',{'skills':skillsToList(job.skills),'job': job,'isapplied':True} )
    #         else:
    #             return render(request,'applicant/job_details.html', context)
    # elif request.method == 'POST' and not user.is_authenticated:
    #     return redirect("login")











    ###################################################################################################
    #                                    web scrapping                                                #
    #                                    from indeed                                                  #
    ###################################################################################################

import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd

class WebCrawler(object):

    def __init__(self, title = '',location = ""):

        self._url = "https://eg.indeed.com/jobs"
        self._headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        self._title = title
        self._location = location
        self.params = {
            'q': self._title,
            'l': self._location,
            
        }

    def get(self):

        try:

            r = requests.get(url=self._url,
                              headers=self._headers ,
                              params=self.params)
            return r.text

        except Exception as e:

            print("Failed to make response to Indeed")



class DataStructure():

    def __init__(self):
        self.data = {
            'title':[],
            'location':[],
            'summary':[],
            'date':[],
            'link' : [],
        }




class DataCleaning(object):

    def __init__(self, title = '', location = ""):
        self._title = title
        self._location = location
        self._webcrawler = WebCrawler(self._title, self._location)
        self.data = self._webcrawler.get()
        self.datastructure = DataStructure()

    def getData(self):
                                                         

        soup = BeautifulSoup(self.data, 'html.parser')                
        dt = soup.find('div', class_="pagination")                      
        for x in str(dt).split():                                       

            if 'data-pp' in x:
                data = x.split("=")
                token = data[1]

                url = "https://eg.indeed.com/jobs"

                headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

        
                
                params = {
                    'q': self._title,
                    'l': self._location,
                    
                    'pp':data[1]
                }
                r = requests.get(url=url,
                                 headers=headers,
                                 params=params)

                textdata = r.text
                soup = BeautifulSoup(self.data, 'html.parser')
                for x in soup.findAll('div', class_="jobsearch-SerpJobCard unifiedRow row result"):
                    title = x.find(class_="title").text.strip()
                    self.datastructure.data["title"].append(title)


                    location = x.find(class_="location accessible-contrast-color-location").text.strip()
                    self.datastructure.data["location"].append(location)


                    summary = x.find(class_="summary")
                    
                    self.datastructure.data["summary"].append(summary.text)

                    date = x.find(class_="date")
                    self.datastructure.data["date"].append(date.text)


                    link = x.find('a', href=True)
                    base_url = "https://eg.indeed.com"


                    Final = base_url + link["href"]
                    #print(Final)
                    self.datastructure.data["link"].append(Final)

            
        data = list(zip(
            self.datastructure.data["title"],  self.datastructure.data["location"],
            self.datastructure.data["summary"],self.datastructure.data["date"],
            self.datastructure.data["link"]
        ))
        df = pd.DataFrame(data=data, columns=["title", "location", "summary", "date", "link" ])
        return df




class IndeedJobSearch(object):

    def __init__(self, title = '', location = ""):

        self.title = title
        self.location = location
        self.datacleaning = DataCleaning(title=self.title, location=self.location)

    def getJobs(self):
        data = self.datacleaning.getData()
        return data
    def saveCsv(self):

        data = self.datacleaning.getData()
        data.to_csv("Jobs.csv")


def showResult(request):
    info = Profile.objects.get(author_id=request.user.id  )
    print("MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM:: ",info)
    t = str(info.job_title)
    z = str(info.address)
    jobsearch = IndeedJobSearch(title=t, location=z)
    data = jobsearch.getJobs()
    context = {
        'data' : data,
        
        
    }
    return render(request,'applicant/recommendation_indeed.html',context)
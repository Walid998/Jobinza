from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse , HttpResponseRedirect
from django.utils import timezone
import datetime
from dateutil.parser import parse
import time
import pytz
from django.contrib.auth.models import User
from django.conf import settings
from company.models import CreatePost, Match_Results , Notification , category
from company.forms import CreatePostForm , SendEmailForm 
from django.contrib.auth.decorators import login_required
from account.decorators import allowed_users , unauthenticated_user
from account.models import Profile
from company.forms import editprofileForm
from django.views.generic import UpdateView,DeleteView 
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.core.mail import EmailMessage
from django.template.loader import get_template
import os
from django.core.paginator import Paginator
from Jobinza.utils import PaginatorX


def skillsToList(txt):
	lst = list()
	t=''
	for i in txt:
		if i != ',':
			t=t+i
		else:
			t=t.strip()
			lst.append(t.lower())
			t=''
	return lst


#def create_post_view(request):
#	context = {}
#	user = request.user
#	form = CreatePostForm(request.POST or None, request.FILES or None)
#	deadline = request.POST.get('deadline')
#	form.deadline = datetime.strptime(deadline, '%Y-%m-%d')
#	if form.is_valid():
#		obj = form.save(commit=False)
#		author = User.objects.filter(email=user.email).first()
#		obj.author = author
#		obj.skills = obj.skills.lower()
#		obj.save()
#		form = CreatePostForm()


#	context['form'] = form
#	return render(request, "company/create_post.html" , context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['employeer'])
def create_post_view(request):
	user = request.user
	categories = category.objects.all()
	#form = CreatePostForm(request.POST or None, request.FILES or None)
	if request.method =='POST':
		form = CreatePostForm(request.POST or None, request.FILES or None)
		form.jobtitle= request.POST.get('jobtitle')
		form.job_description = request.POST.get('job_description')
		form.joblocation = request.POST.get('joblocation')
		form.city = request.POST.get('city')
		form.Area = request.POST.get('Area')
		form.careerlevel = request.POST.get('careerlevel')
		form.jobtype = request.POST.get('jobtype')
		form.salary_range1 = request.POST.get('salary_range1')
		form.salary_range2 = request.POST.get('salary_range2')
		form.num_vacancies = request.POST.get('num_vacancies')
		form.year_of_experience = request.POST.get('year_of_experience')
		form.deadline = request.POST.get('deadline')
		form.category = request.POST.get('category')
		pic = ''
		try:
			com = Profile.objects.get(author = user.id)
			pic = com.image
		except:
			print('>>>company has no photo')
		#form.image = request.FILES.get('image')
		if form.is_valid():
			obj = form.save(commit=False)
			obj.image= pic
			author = User.objects.filter(email=user.email).first()
			obj.author = author
			obj.skills = obj.skills.lower()
			obj.save()		
			Notification.objects.create(receiver=request.user , verb= obj.jobtitle ,  description = "post is created" , post=obj.id )	

	form = CreatePostForm()
	return render(request, "company/create_post.html" ,{'form': form , 'categories':categories})

@login_required(login_url='login')
@allowed_users(allowed_roles=['employeer' , 'applicant'])
def update_status(request):
	now = datetime.date.today()
	form = CreatePost.objects.all()
	for doc in form :
		if doc.status != 'closed':
			if  doc.deadline < now or doc.deadline == now  :
				doc.status = 'closed'
				Notification.objects.create(receiver=doc.author , verb= doc.jobtitle ,  description = "Post is Closed " , post=doc.id )	
			else :
				doc.status = 'Publishing'
			doc.save()

@login_required(login_url='login')
@allowed_users(allowed_roles=['employeer'])
def list_job_view(request):
	update_status(request)
	listpost = CreatePost.objects.all().filter(author= request.user.id)
	categories = []
	for post in listpost:
		category = post.category_id
		categories.append(category)
	categories = list(dict.fromkeys(categories))

	x = len(listpost)
	close = CreatePost.objects.all().filter(author= request.user.id,status='closed')
	y =len(close)
	open = CreatePost.objects.all().filter(author= request.user.id,status='Publishing')
	z =len(open)
	listpost = PaginatorX(request,listpost,5)
	context = {
		'title' : 'list jobs',
		'posts' : listpost,
		'contact' : x,
		'clo' : y,
		'ope' : z,
		'categories':categories
	}
	
	return render(request,"company/list_job.html", context)


#list posts with specific category 
@login_required(login_url='login')
@allowed_users(allowed_roles=['employeer'])
def category_posts(request , category_name):
	categories = []
	list_posts = CreatePost.objects.all().filter(author= request.user.id)
	posts = list_posts.filter( category_id = category_name)
	x = len(posts)
	close = posts.filter(author= request.user.id,status='closed')
	y =len(close)
	open = posts.filter(author= request.user.id,status='Publishing')
	z =len(open)

	for post in list_posts:
		category = post.category_id
		categories.append(category)
	categories = list(dict.fromkeys(categories))

	paginator = Paginator(posts , 4)
	page = request.GET.get('page')
	posts = paginator.get_page(page)

	context = {
		'posts': posts,
		'contact' : x,
		'clo' : y,
		'ope' : z,
		'category_name' : category_name,
		'categories' :categories
	}
	return render(request,"company/list_categoryPosts.html", context)


#jod details

def job_details(request , job_id):
	id_num = int(job_id)
	readone_notification(id_num)
	job_list = CreatePost.objects.get(id=id_num)
	list_applicants = Match_Results.objects.all().filter(job_id=job_id)
	context = {
		'skills':skillsToList(job_list.skills),
		'job': job_list ,
		'applicants':list_applicants
		}
	return render(request,'company/job_details.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['employeer'])
def job_edit(request, job_id):
	id_num = int(job_id)
	jobpost = CreatePost.objects.get(id = id_num)
	context ={
		'job':jobpost,
		'skills':skillsToList(jobpost.skills)
		}
	job_form = CreatePostForm(request.POST or None, instance = jobpost)
	if job_form.is_valid():
		obj = job_form.save(commit=False)
		obj.skills=  obj.skills.lower()
		obj.save()
		messages.success(request,f'Job \"{jobpost.jobtitle}\" has been updated successfully !!')
		update_status(request)
		return redirect(f'/company/details/{jobpost.id}')

	return render(request,'company/edit_post.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['employeer'])	
def job_state_closed(request , job_id):
	id_num = int(job_id)
	job = CreatePost.objects.get(id=id_num)
	if job.status != 'closed':
		job.deadline = datetime.date.today()
		job.status = 'closed'
		messages.warning(request ,f'Job \"{job.jobtitle}\" has been closed !!')
		job.save()
	return redirect(f'/company/details/{job.id}')

@login_required(login_url='login')
@allowed_users(allowed_roles=['employeer'])
def job_state_open(request , job_id ):
	id_num = int(job_id)
	job = CreatePost.objects.get(id=id_num)
	if request.method == 'POST':
		job.deadline = request.POST.get('deadline')
		job.status = 'Publishing'
		messages.info(request,f'Job \"{job.jobtitle}\" has been published !!')	
		job.save()
	return redirect(f'/company/details/{job.id}')


@login_required(login_url='login')
@allowed_users(allowed_roles=['employeer'])
def job_delete(request, job_id):
	job_id = int(job_id)
	try:
		job = CreatePost.objects.get(id = job_id)
		tit= job.jobtitle	
		if job.delete():
			messages.success(request,f'Job \" {tit} \" has been deleted !!')
			return redirect('/company/list')
	except CreatePost.DoesNotExist:
		return redirect('/company/list')

#publish job
@login_required(login_url='login')
@allowed_users(allowed_roles=['employeer'])
def list_job_publish_view(request):
	update_status(request)
	listpost = CreatePost.objects.all().filter(author= request.user.id,status='Publishing')
	context = {
		'title' : 'list jobs',
		'posts' : listpost,
	}
	
	return render(request,"company/list_job_publish.html", context)


#close job
@login_required(login_url='login')
@allowed_users(allowed_roles=['employeer'])
def list_job_close_view(request):
	update_status(request)
	listpost = CreatePost.objects.all().filter(author= request.user.id,status='closed')
	context = {
		'title' : 'list jobs',
		'posts' : listpost,
		}

	return render(request,"company/list_job_closed.html", context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['employeer'])
def profile_info(request,user_name):
    user_info = User.objects.get(username=user_name)
    pk = User.objects.get(username=user_name).pk
    try:
        p_info = Profile.objects.get(author = pk)
        return render(request,'company/profile.html', {'result': user_info , 'info':p_info } )
    except:
        return render(request,'company/profile.html', {'result': user_info , 'info':'' })


@login_required(login_url='login')
@allowed_users(allowed_roles=['employeer'])
def editProfile (request):    
	if request.method == 'POST':
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
				return redirect(f'/company/profile/{request.user}')
		except:
			form = editprofileForm(request.POST , request.FILES)
			if form.is_valid():
				print("<<< pinfo has no data >>>")
				inst = Profile()
				inst.image = request.FILES.get('image')
				print ('**************************',inst.image)
				inst.phonenumber = form.cleaned_data.get('phonenumber')
				inst.address = form.cleaned_data.get('address')
				inst.location = form.cleaned_data.get('location')
				inst.description = form.cleaned_data.get('description')
				inst.author = auth
				inst.save()
				return redirect(f'/company/profile/{request.user}')

@login_required(login_url='login')
@allowed_users(allowed_roles=['employeer'])
def send_email(request,user_name):
	Send_Form = SendEmailForm
	applicant = User.objects.get(username = user_name)
	print("<<<>>>>>>>>>>>>>  ",applicant.email)
	if request.method == 'POST':
		form = Send_Form(data=request.POST)
        
		if form.is_valid():
			username = request.POST.get('username')
			emails = request.POST.get('email')
			content = request.POST.get('content')

			template = get_template('company/send_form.txt')
			context = {
					'username' : username,
					'email' : emails,
					'content' : content,
			}
					
			content = template.render(context)

			email = EmailMessage(
					"New contact form email",
					content,
					"jobinza web" + '',
					[emails],
					headers = { 'Reply To': emails }
			)
			email.send()

	return render(request,'company/send_email.html',{'applicant':applicant})

@login_required(login_url='login')
@allowed_users(allowed_roles=['employeer'])
def readall_notification(request):
	Notifications = Notification.objects.all().filter(receiver = request.user.id)
	for n in Notifications :
		if n.read == False:
			n.read = True
			n.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def readone_notification(job_id):
	Noti = Notification.objects.get(post = job_id)
	if Noti.read == False:
		Noti.read = True
		Noti.save()


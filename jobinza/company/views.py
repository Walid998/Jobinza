from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from django.utils import timezone
import datetime
from dateutil.parser import parse
import time
import pytz
from django.contrib.auth.models import User
from django.conf import settings
from company.models import CreatePost, Match_Results
from company.forms import CreatePostForm
from django.contrib.auth.decorators import login_required
from account.decorators import allowed_users , unauthenticated_user
from django.views.generic import UpdateView,DeleteView 
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.contrib import messages
from django.utils.dateparse import parse_date

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

@login_required(login_url='login')
@allowed_users(allowed_roles=['applicant' , 'employeer'])
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

def create_post_view(request):
	context = {}
	user = request.user
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
		form.image = request.FILES.get('image')
		print(form.deadline)
		#form.deadline = datetime.datetime.strptime(deadline , 'YYYY-mm-ddTHH:MM:ssZ')
		#date_processing = deadline.replace('T', '-').replace(':', '-').split('-')
		#date_processing = [int(v) for v in date_processing]
		#form.deadline = datetime.datetime(*date_processing)
		#form.deadline = datetime.datetime(*[int(v) for v in deadline.replace('T', '-').replace(':', '-').split('-')])
		if form.is_valid():
			obj = form.save(commit=False)
			author = User.objects.filter(email=user.email).first()
			obj.author = author
			obj.skills = obj.skills.lower()
			obj.save()

	form = CreatePostForm()
	context['form'] = form
	return render(request, "company/create_post.html" , context)

#def update_status():
#	now = datetime.date.today()
#	form = CreatePost.objects.all()
#	for doc in form :
#		if doc.deadline < now or doc.deadline == now:
#			doc.status = 'closed'
#		doc.save()
 

def update_status():
	now = datetime.date.today()
	form = CreatePost.objects.all()
	for doc in form :
		if doc.deadline < now or doc.deadline == now:
			doc.status = 'closed'
		else :
			doc.status = 'Publishing'
		doc.save()


@login_required(login_url='login')
def list_job_view(request):
	update_status()
	listpost = CreatePost.objects.all().filter(author= request.user.id)
	x = len(listpost)
	close = CreatePost.objects.all().filter(author= request.user.id,status='closed')
	y =len(close)
	open = CreatePost.objects.all().filter(author= request.user.id,status='Publishing')
	z =len(open)
	
	context = {
		'title' : 'list jobs',
		'posts' : listpost,
		'contact' : x,
		'clo' : y,
		'ope' : z,
	}
	
	return render(request,"company/list_job.html", context)

#jod details
def job_details(request , job_id):
	id_num = int(job_id)
	job_list = CreatePost.objects.get(id=id_num)
	list_applicants = Match_Results.objects.all().filter(job_id=job_id)
	context = {
		'skills':skillsToList(job_list.skills),
		'job': job_list ,
		'applicants':list_applicants
		}
	return render(request,'company/job_details.html', context)

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
		update_status()
		return redirect(f'/company/details/{jobpost.id}')

	return render(request,'company/edit_post.html',context)
	
def job_state_closed(request , job_id):
	id_num = int(job_id)
	job = CreatePost.objects.get(id=id_num)
	if job.status != 'closed':
		job.deadline = datetime.date.today()
		job.status = 'closed'
		messages.warning(request ,f'Job \"{job.jobtitle}\" has been closed !!')
		job.save()
	return redirect(f'/company/details/{job.id}')

	""" else :
		if request.method == 'POST':
			job.deadline == request.POST.get('deadline')		
			job.status = 'Publishing'
			messages.info(request,f'Job \"{job.jobtitle}\" has been published !!')	 """
		
def job_state_open(request , job_id , deadline):
	id_num = int(job_id)
	print(deadline)
	#dead = datetime.datetime.strptime(deadline , "%d-%m-%Y")
	job = CreatePost.objects.get(id=id_num)
	if job.status == 'closed' and deadline != None:
		job.deadline = deadline
		job.status = 'Publishing'
		messages.info(request,f'Job \"{job.jobtitle}\" has been published !!')	
		job.save()
	return redirect(f'/company/details/{job.id}')


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
def list_job_publish_view(request):
	update_status()
	listpost = CreatePost.objects.all().filter(author= request.user.id,status='Publishing')
	context = {
		'title' : 'list jobs',
		'posts' : listpost,
	}
	
	return render(request,"company/list_job_publish.html", context)


#close job
@login_required(login_url='login')
def list_job_close_view(request):
	update_status()
	listpost = CreatePost.objects.all().filter(author= request.user.id,status='closed')
	context = {
		'title' : 'list jobs',
		'posts' : listpost,
		}

	return render(request,"company/list_job_closed.html", context)

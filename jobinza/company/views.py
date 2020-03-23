from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from django.conf import settings
from company.models import CreatePost
from company.forms import CreatePostForm
from django.contrib.auth.decorators import login_required
from account.decorators import allowed_users , unauthenticated_user
from django.views.generic import UpdateView,DeleteView 
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.contrib import messages

def skillsToList(txt):
	lst = list()
	t=''
	for i in txt:
		if i != ',':
			t=t+i
		else:
			t=t.strip()
			lst.append(t)
			t=''
	return lst

@login_required(login_url='login')
@allowed_users(allowed_roles=['applicant' , 'employeer'])
def create_post_view(request):
	context = {}
	user = request.user
	form = CreatePostForm(request.POST or None, request.FILES or None)
	
	if form.is_valid():
		obj = form.save(commit=False)
		author = User.objects.filter(email=user.email).first()
		obj.author = author
		obj.skills = obj.skills.lower()
		obj.save()
		form = CreatePostForm()

	context['form'] = form
	return render(request, "company/create_post.html" , context)


def update_status():
	now = datetime.date.today()
	form = CreatePost.objects.all()
	for doc in form :
		if doc.deadline < now or doc.deadline == now:
			doc.status = 'closed'
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
	listjob = CreatePost.objects.all()
	context = {
		'skills':skillsToList(job_list.skills),
		'job': job_list ,
		'posts':listjob
		}
	return render(request,'company/job_details.html', context)

def job_edit(request, job_id):
	job = jobRole.objects.all()
	industry = relatedIndustry.objects.all()
	skill = skills.objects.all()
	id_num = int(job_id)
	jobpost = CreatePost.objects.get(id = id_num)
	job_form = CreatePostForm(request.POST or None, instance = jobpost)
	if job_form.is_valid():
		job_form.save()
		messages.success(request,f'Job \"{jobpost.jobtitle}\" has been updated successfully !!')
		return redirect(f'/company/details/{jobpost.id}')
	return render(request,'company/edit_post.html',{'job':jobpost,'jobs':job , 'industries': industry , 'skills':skill})
	
def job_state_closed(request , job_id):
    id_num = int(job_id)
    job = CreatePost.objects.get(id=id_num)
    if job.status != 'closed':
        job.status= 'closed'
        messages.warning(request,f'Job \"{job.jobtitle}\" has been closed !!')
    else:
        job.status= 'Publishing'
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

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from django.utils import timezone
import datetime
from django.contrib.auth.models import User

from company.models import CreatePost , jobRole , relatedIndustry
from company.forms import CreatePostForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def create_post_view(request):
	job = jobRole.objects.all()
	industry = relatedIndustry.objects.all()
	#job = ['business' , 'engineer']
	context = {}
	user = request.user
	form = CreatePostForm(request.POST or None, request.FILES or None)
	
	if form.is_valid():
		obj = form.save(commit=False)
		author = User.objects.filter(email=user.email).first()
		obj.author = author
		obj.save()
		#return render(request, "company/create_post.html")
		form = CreatePostForm()

	context['form'] = form
	#return render(request, "company/list_job.html")
	return render(request, "company/create_post.html" , {'jobs':job , 'industries': industry} , context)

def addjobRole_view (request):
	if request.method == 'POST':
		job = jobRole()
		job.name = request.POST.get('role')
		job.save()

	return  render(request, "company/jobrole.html" )

def addRelatedIndustry_view (request):
	if request.method == 'POST':
		job = relatedIndustry()
		job.name = request.POST.get('related_industry')
		job.save()

	return  render(request, "company/relatedindustry.html" )


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
	listpost = CreatePost.objects.all()
	context = {
		'title' : 'list jobs',
		'posts' : listpost,
	}
	return render(request,"company/list_job.html", context)


	

		




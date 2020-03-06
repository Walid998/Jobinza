from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from django.utils import timezone
import datetime
from django.contrib.auth.models import User

from company.models import CreatePost , jobRole , relatedIndustry , skills
from company.models import CreatePost
from company.forms import CreatePostForm
from django.contrib.auth.decorators import login_required
from account.decorators import allowed_users , unauthenticated_user
from django.views.generic import UpdateView,DeleteView 
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin


@login_required(login_url='login')
@allowed_users(allowed_roles=['applicant'])
def create_post_view(request):
	job = jobRole.objects.all()
	industry = relatedIndustry.objects.all()
	skill = skills.objects.all()
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

	return render(request, "company/create_post.html" , {'jobs':job , 'industries': industry , 'skills':skill} , context)



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

def addskill_view (request):
	if request.method == 'POST':
		job = skills()
		job.name = request.POST.get('skills')
		job.save()

	return  render(request, "company/skills.html" )


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

#jod details
def job_details(request , job_id):
    job =None
    id_num = int(job_id)
    job_list = CreatePost.objects.get(id=id_num)
    return render(request,'company/job_details.html', {'job': job_list})


# upate view for details
class PostUpdateView(UserPassesTestMixin,LoginRequiredMixin, UpdateView):
	model = CreatePost
	template_name = 'company/list/post_update.html'
	form_class = CreatePostForm
	def form_invalid(self,form):
		form.instance.author = self.request.user
		return super().form_invalid(form)

	def test_func(self):
		post=self.get_object()
		if self.request.user == CreatePost.author:
			return True
		else:	
			return False
	

# delete view for details 
class PostDeleteView(UserPassesTestMixin,LoginRequiredMixin,DeleteView):
	model = CreatePost
	success_url = 'company/list/'
	def test_func(self):
		post=self.get_object()
		if self.request.user == CreatePost.author:
			return True
		return False
	

		




#from django.shortcuts import render

# Create your views here.
#def home(request):
#    context = { 
#        'title': 'home',
#    }
#    return render(request,'company/index.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse

from company.models import CreatePost
from company.forms import CreatePostForm
from account.models import Account
from django.contrib.auth.decorators import login_required

<<<<<<< HEAD
@login_required(login_url='login')
=======

>>>>>>> a2b1d189fc09fb3721035d456ca40fd9398dd0dd
def create_post_view(request):

	context = {}
	user = request.user
	form = CreatePostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		author = Account.objects.filter(email=user.email).first()
		obj.author = author
		obj.save()
		form = CreatePostForm()

	context['form'] = form
	return render(request, "company/create_post.html", context)



def list_job_view(request):
	listpost = CreatePost.objects.all()
	context = {
		'title' : 'list jobs',
		'posts' : listpost,
	}
	return render(request,"company/list_job.html", context)


	

		




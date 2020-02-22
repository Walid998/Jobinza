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
from company.models import Listshow


#posts =
 #[
		#{
		#	'title':'tester',
		#	'place' : 'cairo',
		#	'post_date' : '20-2-2020',
		#	'author' : 'wesam'
		#},
		#{
		#	'title':'accounting',
		#	'place' : 'cairo',
		#	'post_date' : '16-2-2020',
		#	'author' : 'sozan'
		#},
		#{
		#	'title':'developer',
		#	'place' : 'cairo',
		#	'post_date' : '13-2-2020',
		#	'author' : 'osama'
		#},
		#{
		#	'title':' designer',
		#	'place' : 'cairo',
		#	'post_date' : '15-2-2020',
		#	'author' : 'amgad'
		#},
	#]






def create_post_view(request):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')

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
	context = {
		'title' : 'Dashboard',
		'posts' : Listshow.objects.all()
	}
	return render(request,"company/list_job.html", context)


	

		




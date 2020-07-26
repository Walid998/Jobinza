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
from company.models import CreatePost, Match_Results , Notification , category,Schdule
from company.forms import CreatePostForm , SendEmailForm ,SchduleForm
from django.contrib.auth.decorators import login_required
from account.decorators import allowed_users , unauthenticated_user
from account.models import Profile 
from account.forms import AccountSettingForm
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
		category_name = request.POST.get('category')
		cat = category.objects.get(name = category_name)
		if cat.jobno == None:
			cat.jobno = 1
		else:
			cat.jobno = cat.jobno +1
		cat.save()
		print("<><<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ",type(cat.jobno))
		# cat.jobno =cat.jobno + 1
		# cat.save()
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
			Notification.objects.create(receiver=obj.author , verb= "Posting" ,  description = obj.jobtitle + " Post is Closed " , post=obj.id )	
			return redirect(f'/company/list')
		
	profile = ""
	form = CreatePostForm()

	try :
		pro = Profile.objects.get(author_id=request.user.id)
		if pro.address and pro.phonenumber and pro.description and pro.image and pro.location:
			profile = "complete"
		else :
			profile = "uncomplete"
	except :
		print("no profile")
		profile = "uncomplete"

	return render(request, "company/create_post.html" ,{'form': form , 'categories':categories , 'profile' : profile , 'user' : user})

@login_required(login_url='login')
@allowed_users(allowed_roles=['employeer' , 'applicant'])
def update_status(request):
	now = datetime.date.today()
	form = CreatePost.objects.all()
	for doc in form :
		if doc.status != 'closed':
			if  doc.deadline < now or doc.deadline == now  :
				doc.status = 'closed'
				Notification.objects.create(receiver=doc.author , verb= "Posting" ,  description = doc.jobtitle + "Post is Closed " , post=doc.id )	
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
	close = listpost.filter(author= request.user.id,status='closed')
	y =len(close)
	open = listpost.filter(author= request.user.id,status='Publishing')
	z =len(open)
	listpost = PaginatorX(request,listpost,5)
	user = request.user
	try :
		profile = Profile.objects.get(author_id = user.id )
	except:
		profile=""
	#closepost = PaginatorX(request,close,3)
	#openpost = PaginatorX(request,open,1)
	context = {
		'title' : 'list jobs',
		'posts' : listpost,
		'contact' : x,
		'clo' : y,
		'ope' : z,
		'categories':categories,
		'open':open,
		'close': close,
		'profile':profile
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

	user = request.user
	try :
		profile = Profile.objects.get(author_id = user.id )
	except:
		profile=""

	context = {
		'posts': posts,
		'contact' : x,
		'clo' : y,
		'ope' : z,
		'category_name' : category_name,
		'categories' :categories,
		'profile':profile
	}
	return render(request,"company/list_categoryPosts.html", context)


#jod details
@login_required(login_url='login')
@allowed_users(allowed_roles=['employeer'])
def job_details(request , job_id):
	id_num = int(job_id)
	readone_notification(request.user.id , id_num , 'Posting')
	job_list = CreatePost.objects.get(id=id_num)
	
	list_applicants = Match_Results.objects.all().filter(job_id=job_id).order_by('-skills_rslt')
	schudle_user = Match_Results.objects.all().filter(status = 'Accepted' , company = request.user.id)
	form = SchduleForm(request.POST or None )
	if request.method == 'POST':
		if form.is_valid():
			scc = Schdule()
			scc.author = request.user.id
			scc.username = request.POST.get('username')
			scc.jobname = request.POST.get('jobname')
			scc.date_schdule = request.POST.get('date_schdule')
			scc.time_schdule = request.POST.get('time_schdule')
			scc.save()
		else:
			print("form not not not not valid ")
	context = {
		'skills':skillsToList(job_list.skills),
		'job': job_list ,
		'applicants':list_applicants,
		'schudle_user' : schudle_user,
		}
	return render(request,'company/job_details.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['employeer'])
def job_edit(request, job_id):
	id_num = int(job_id)
	jobpost = CreatePost.objects.get(id = id_num)
	list_category = category.objects.all()
	list_jobtype = ['Full Time', 'Part Time' , 'Freelance' , 'From Home' , 'Volunteering' ]
	list_CareerLevel = ['Student', 'Entry level' , 'Experienced' , 'Manager' , 'Senior Manager' ]
	context ={
		'job':jobpost,
		'skills':skillsToList(jobpost.skills),
		'categories':list_category,
		'jobtype':list_jobtype,
		'careerlevel':list_CareerLevel,
		}
	job_form = CreatePostForm(request.POST or None, instance = jobpost)
	if job_form.is_valid():
		obj = job_form.save(commit=False)
		obj.skills=  obj.skills.lower()
		obj.save()
		messages.success(request,f'Job \"{jobpost.jobtitle}\" has been updated successfully !!')
		update_status(request)
		return redirect(f'/company/details/{jobpost.id}')
	else:
		print("FFFFFFFFFFFFFF>>>>>>> form not valid")
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['employeer' , 'applicant'])
def profile_info(request,user_name):
	user_info=User.objects.get(username=user_name)
	pk = User.objects.get(username=user_name).pk
	try:
		p_info=Profile.objects.get(author=pk)
		return render(request,'company/profiles.html', {'result': user_info , 'info':p_info ,'schudle_info':Schdule.objects.filter(author=request.user.id)
		,'count_jobs':CreatePost.objects.filter(author_id = request.user.id).count(),
		'pending' : Match_Results.objects.filter(status='pending',company=request.user.id).count(),
		'accepted': Match_Results.objects.filter(status='Accepted',company=request.user.id).count(),
		'user_company':Match_Results.objects.filter(company=request.user.id , status = 'Accepted'),})
	except:
		return render(request,'company/profiles.html', {'result': user_info , 'info':'' ,'schudle_info':Schdule.objects.filter(author=request.user.id)
		,'count_jobs':CreatePost.objects.filter(author_id = request.user.id).count(),
		'pending' : Match_Results.objects.filter(status='pending',company=request.user.id).count(),
		'accepted': Match_Results.objects.filter(status='Accepted',company=request.user.id).count(),
		'user_company':Match_Results.objects.filter(company=request.user.id , status = 'Accepted'),})

@login_required(login_url='login')
@allowed_users(allowed_roles=['employeer'])
def editProfile (request):
	uname = request.user
	auth = User.objects.get(username=uname)
	pk = User.objects.get(username=uname).pk
	readone_notification(auth , '' , "Welcome")

	pinfo = ''
	try:
		pinfo = Profile.objects.get(author = pk)   
	except:
		print('no profile')

	if request.method == 'POST':
		try:
			pinfo = Profile.objects.get(author = pk)  
			print("***********<<<<<<< pinfo has data >>>>>>>***********")
			form = editprofileForm(request.POST)
			if form.is_valid():
				pinfo.phonenumber = form.cleaned_data.get('phonenumber')
				pinfo.address = form.cleaned_data.get('address')
				pinfo.location = form.cleaned_data.get('location')
				pinfo.description = form.cleaned_data.get('description')
				pinfo.save()
				return redirect(f'/company/profile/{request.user}')
                #messages.success(request,f'Job has been updated successfully !!')
		except:
			form = editprofileForm(request.POST)
			if form.is_valid():
				print("<<< pinfo has no data >>>")
				inst = Profile()
				#inst.image = request.FILES.get('image')
				#print ('**************************',inst.image)
				inst.phonenumber = form.cleaned_data.get('phonenumber')
				inst.address = form.cleaned_data.get('address')
				inst.location = form.cleaned_data.get('location')
				inst.description = form.cleaned_data.get('description')
				inst.author = auth
				#auth_user.username = form1.cleaned_data.get('username')
				#auth_user.first_name = form1.cleaned_data.get('first_name')
				#auth_user.last_name = form1.cleaned_data.get('last_name')
				#auth_user.email = form1.cleaned_data.get('email')
				inst.save()
				return redirect(f'/company/edit_profile/')
	return render(request,'company/edit_profile.html',{'result':auth , 'info' : pinfo ,})

@login_required(login_url='login')
@allowed_users(allowed_roles=['employeer'])
def send_email(request,user_name,job_id):
	Send_Form = SendEmailForm
	applicant = User.objects.get(username = user_name)
	stat = Match_Results.objects.get(id = job_id)
	job = CreatePost.objects.get(id = job_id)
	if stat.status != 'Accepted':
		stat.status='Accepted'
		stat.save()
	elif stat.status != 'Rejected':
		stat.status = 'Rejected'
		stat.save()

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
			Notification.objects.create(receiver=applicant , verb= "Posting" ,  description = " You recieved an email about " + job.jobtitle + " job . Please check your mail" , post=job_id )	


	return render(request,'company/send_email.html',{'applicant':applicant,"stat" : stat})

def send_emails(content,to):
	email = EmailMessage(
		"New contact form email",
		content,
		"jobinza web" + '',
		[to],
		headers = { 'Reply To': to }
	)
	email.send()

def contentmessage(applicant,company,job_title,app_status):
	content = ""
	if app_status == 'Accepted':
		content = f'''Congratulations {applicant} !!, you have been accepted to have an interview in {company.capitalize()} company according to your apply request for {job_title} job , you will recieve another email inform you the appointment and location soon. Good Luck !! '''
	elif app_status == 'Rejected':
			content = f'''Dear {applicant}, we are sorry to tell you that your apply request for {job_title} job has been rejected because your qualifications not match our job requirements, to have to do your best all time and you're able to apply again after 3 monthes. Good Luck !! - company: {company.capitalize()}.'''
	return content

def selected_applicants(request,company,job_title,app_status):
	if request.method == 'POST' and (request.POST.get('applicants_emails') != None):
		print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^before send email :: ')
		emls = str(request.POST.get('applicants_emails'))
		lst = skillsToList(emls)
		content= ""
		for app_email in lst:
			applicant = Match_Results.objects.get(app_email = app_email)
			app_name = User.objects.get(username = applicant.aplcnt)
			applicant.status = app_status
			applicant.save()
			content = contentmessage(app_name.username ,company,job_title,app_status)
			print("KKMMKKMMDDFFDDFFZZZZZZZZZZZZZZ<<<<<<<<<< :: ",content)
			send_emails(content,app_email)
			Notification.objects.create(receiver=applicant.aplcnt , verb= "Posting" ,  description = "You recieved an Email about "  + job_title + " job . Please Check Your mail " , post=applicant.job_id )	

		print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^after send email ')
		return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
	else:
		print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^OOOOOOOLLL::::: No EMails ')
		return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
		
########################################################
########################################################
########################################################
@login_required(login_url='login')
@allowed_users(allowed_roles=['employeer'])
def status_accepted(request ,pk):
	statu = Match_Results.objects.get(id=pk)
	statu.status = 'Accepted'
	messages.info(request,f'applicant has been Accepted !!')	
	statu.save()
	context = {'statu':statu,id:pk}	
	return redirect('/company/list')



@login_required(login_url='login')
@allowed_users(allowed_roles=['employeer'])	
def status_rejected(request , pk):
	statu = Match_Results.objects.get(id=pk)
	statu.status = 'Rejected'
	messages.warning(request ,f'applicant  has been Rejected !!')
	statu.save()
	context = {'statu':statu , id:pk}
	return redirect('/company/detials')
########################################################
########################################################
########################################################

@login_required(login_url='login')
def readall_notification(request):
	Notifications = Notification.objects.all().filter(receiver = request.user.id)
	for n in Notifications :
		if n.read == False:
			n.read = True
			n.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def readone_notification(user_id , job_id , Noti_verb):
	if job_id != '':
		Noti = Notification.objects.all().filter(receiver = user_id , post = job_id , verb=Noti_verb)
	else :
		Noti = Notification.objects.all().filter(receiver = user_id , verb=Noti_verb)
	for n in Noti :
		if n.read == False:
			n.read = True
			n.save()

def company_delete(request , id_usr):
	id_usr = request.user.id
	try:
		usr = User.objects.get(id = id_usr)
		if usr.delete():
			messages.success(request,f'employeer \" {request.user.username} \" has been deleted !!')
			return redirect('/company/profile/{{request.user.username}}')
	except User.DoesNotExist:
		return redirect('/company/profile/{{request.user.username}}')
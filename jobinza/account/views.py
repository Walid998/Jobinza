from django.shortcuts import render, redirect
from .forms import UserCreationForm, UserCreationForm2, LoginForm ,AccountSettingForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import unauthenticated_user
from django.contrib.auth.models import Group
from company.models import CreatePost , category
import random
from django.contrib.auth.models import User
from account.models import Profile
from django.core.paginator import Paginator
import base64
def account_setting(request , user_id):
    id_num = int(user_id)
    us = User.objects.get(id=id_num)
    form = AccountSettingForm(request.POST, instance=request.user)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.username = request.POST.get('username')
            obj.first_name = request.POST.get('first_name')
            obj.last_name = request.POST.get('last_name')
            obj.email = request.POST.get('email')
            obj.save()
        else:
            print("##################errorroroororor")
    return render(request,'account/account_setting2.html' , {'us':us})

def upld_propic(request):
    user = request.user
    usrnm = str(user)
    if request.method == 'POST':
        img = request.POST.get('propic')
        with open("media/profile-pic/company/"+usrnm+"_imageToSave.png", "wb") as fh:
            fh.write(base64.b64decode(img))
        try:
            obj =Profile.objects.get(author = user.id)
            obj.image = "/"+fh.name
            obj.save()
        except:
            obj = Profile()
            obj.image = "/"+fh.name
            obj.author = user
            obj.save()
        
        return redirect ('/company/edit_profile/')

def change_account_setting(request):
    user = request.user
    #us = User.objects.get(id=user.id)
    form = AccountSettingForm(request.POST, instance=user)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            #obj.username = request.POST.get('username')
            obj.first_name = request.POST.get('first_name')
            obj.last_name = request.POST.get('last_name')
            obj.email = request.POST.get('email')
            obj.save()
        else:
            print("##################errorroroororor")
    return redirect('password_change')

@unauthenticated_user
def registration_view(request):
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            username = form.cleaned_data.get('username')
            user = form.save()
            group = Group.objects.get(name='applicant')
            user = form.save()
            user.groups.add(group)
            messages.success(
                request, f'Congrats {username} account created successfully !!')
            return redirect('login')
    else:  
        form = UserCreationForm()
    return render(request, 'account/signup.html', {'title': 'Sign Up','form': form,})

@unauthenticated_user
def registration_view_hr(request):
    if request.method == 'POST':
        form = UserCreationForm2(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            username = form.cleaned_data.get('username')
            user = form.save()
            group = Group.objects.get(name='employeer')
            user = form.save()
            user.groups.add(group)
            messages.success(
                request, f'Congrats {username} account created successfully !!')
            return redirect('login')
    else:  
        form = UserCreationForm2()
    return render(request, 'account/signup.html', {'title': 'Sign Up','form': form,})


@unauthenticated_user
def registration_for_both(request):
    return render(request, 'account/signup.html')



@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.groups.filter(name="employeer").exists():
                return redirect('/company/list')
            elif user.groups.filter(name="applicant").exists():
                return redirect('/applicant/listapp')
        else:
            messages.warning(
                request, 'your username or password isn\'t correct !! ')
    return render(request, 'account/login.html', {
        'title': 'Sign in',
    })

def log(request):
    return render(request, 'account/log.html')

def logout_view(request):
    logout(request)
    return redirect('login')

#@unauthenticated_user
def guestPage(request):
    result = []
    companies = []
    profiles = Profile.objects.all()
    jobs = CreatePost.objects.all().filter(status = "Publishing")
    catagories = category.objects.filter(jobno__gt = 0)

    users = User.objects.all()
    for user in users :
        if user.groups.filter(name="employeer").exists():
            companies.append(user)
    for company in companies :
        for profile in profiles :
            if company.id == profile.author_id:
                result.append(profile)

    paginator = Paginator(jobs,5)
    page = request.GET.get('page')
    jobs = paginator.get_page(page)
    return render(request,'account/guest.html',{'jobs':jobs,'joblength':len(jobs),'users':users , 'profiles': result , 'catagories':catagories})
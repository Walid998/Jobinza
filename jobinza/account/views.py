from django.shortcuts import render, redirect
from .forms import UserCreationForm, UserCreationForm2, LoginForm 
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import unauthenticated_user
from django.contrib.auth.models import Group
from company.models import CreatePost
import random
from django.contrib.auth.models import User
from account.models import Profile
from django.core.paginator import Paginator


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
    return render(request, 'account/register.html', {'title': 'Sign Up','form': form,})

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
    return render(request, 'account/register_hr.html', {'title': 'Sign Up','form': form,})

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

def logout_view(request):
    logout(request)
    return redirect('login')

@unauthenticated_user
def guestPage(request):
    result = []
    companies = []
    profiles = Profile.objects.all()
    jobs = CreatePost.objects.all()
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
    return render(request,'account/guest.html',{'jobs':jobs,'joblength':len(jobs),'users':users , 'profiles': result})
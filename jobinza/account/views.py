from django.shortcuts import render, redirect
from .forms import UserCreationForm,LoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import unauthenticated_user
from django.contrib.auth.models import Group
from company.models import CreatePost

@unauthenticated_user
def registration_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='applicant')
            user.groups.add(group)
            #new_user.save()
            messages.success(
                request, f'Congrats {username} account created successfully !!')
            return redirect('login')
    else:  
        form = UserCreationForm()
    return render(request, 'account/register.html', {
        'title': 'Sign Up',
        'form': form,
    })
@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/company/create')
        else:
            messages.warning(
                request, 'your username or password isn\'t correct !! ')

    return render(request, 'account/login.html', {
        'title': 'Sign in',
    })

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    listpost=CreatePost.objects.all()
    context={
        'title':'home',
        'posts':listpost
    }
    return render(request,'account/home.html',context)
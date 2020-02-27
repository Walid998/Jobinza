from django.shortcuts import render, redirect
from .forms import UserCreationForm,LoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def registration_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            messages.success(
                request, f'Congrats {new_user} account created successfully !!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'account/register.html', {
        'title': 'Sign Up',
        'form': form,
    })

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
	return render(request,'account/home.html')
from django import forms
#from django.contrib.auth import get_user_model
#User = get_user_model()
from django.contrib.auth.models import User
#from .models import Profile

class UserCreationForm(forms.ModelForm):
    name =forms.CharField(label='',max_length=30,widget=forms.TextInput(attrs={'placeholder':'Your Name'}))
    username =forms.CharField(label='',max_length=30,widget=forms.TextInput(attrs={'placeholder':'Username'}))
    email =forms.EmailField(label='',widget=forms.TextInput(attrs={'placeholder':'Your Email'}))
    password1 = forms.CharField(label='',min_length=8,widget=forms.TextInput(attrs={'placeholder':'Password','type':'password'}))
    password2 = forms.CharField(label='',min_length=8,widget=forms.TextInput(attrs={'placeholder':'Password','type':'password'}))
    
    
    class Meta:
        model = User
        fields = ('name','username','email','password1','password2',)
        
    
        

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('passwords not matches')
        return cd['password2']

    def clean_email(self):
        cd=self.cleaned_data
        if User.objects.filter(email=cd['email']).exists():
            raise forms.ValidationError('this email already registered before')
        return cd['email']
    
class LoginForm(forms.ModelForm):
    email = forms.EmailField(label='',widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Password','type':'password'}))

    class Meta:
        model = User
        fields = ('email', 'password')

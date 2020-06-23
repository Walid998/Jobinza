from django import forms
from applicant.models import upload
from applicant.models import contacts
from account.models import Profile
from django.forms import ClearableFileInput

class uploadForm(forms.ModelForm):
    class Meta:
        model = upload
        fields = ['pdf']
        widgets = {
            'pdf': ClearableFileInput(attrs={'multiple': True}),
        }



class editprofileForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    phonenumber = forms.CharField(required=False)
    address = forms.CharField(required=False)
    job_title = forms.CharField(required=False)
    class Meta:
        model = Profile
        fields = [
	
        'image',
        'phonenumber',
        'address',
        'job_title', 			

]


class contactform(forms.Form):
    model = contacts
    fields = [
        'fullname',
        'email',
        'phone',
        'message',
    ]

class SeeJobsForm(forms.Form):
    job_title = forms.CharField(required=True)
    city = forms.CharField(required=False)
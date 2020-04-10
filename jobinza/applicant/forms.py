from django import forms
from applicant.models import upload
from applicant.models import contacts
from account.models import Profile
class uploadForm(forms.ModelForm):
    class Meta:
        model = upload
        fields = ( 'pdf', )



class editprofileForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    phonenumber = forms.CharField(required=False)
    address = forms.CharField(required=False)
    class Meta:
        model = Profile
        fields = [
	
        'image',
        'phonenumber',
        'address', 			

]


class contactform(forms.Form):
    model = contacts
    fields = [
        'fullname',
        'email',
        'phone',
        'message',
    ]
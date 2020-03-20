from django import forms
from applicant.models import upload
from applicant.models import contacts
class uploadForm(forms.ModelForm):
    class Meta:
        model = upload
        fields = ( 'pdf', )


class contactform(forms.Form):
    model = contacts
    fields = [
        'fullname',
        'email',
        'phone',
        'message',
    ]
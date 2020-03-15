from django import forms
from applicant.models import upload

class uploadForm(forms.ModelForm):
    class Meta:
        model = upload
        fields = ( 'pdf', )